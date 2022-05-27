# Convert between different CSV formats
import os
import string
from collections import defaultdict
from InquirerPy import inquirer
from tabulate import tabulate
import chardet as chardet
import pandas as pd
from tqdm.auto import tqdm
from click import secho
from yaspin import yaspin

from .common.csv_rw import select_input, select_output
from bs4.dammit import EncodingDetector, UnicodeDammit


def convert_csv(input_dir=None):
    if not input_dir:  # Set default input directory
        input_dir = os.getcwd()

    # Get input file
    input_file = select_input(input_dir)
    if not input_file:
        return

    # Get output file
    default_output = os.path.basename(input_file.replace('.csv', '_converted.csv'))
    output_file = select_output(default_output)
    if output_file == default_output:  # Append working dir if default
        output_file = os.path.join(input_dir, default_output)

    # Detect Encoding
    result = defaultdict(int)
    with open(input_file, 'rb') as rawdata:
        for line in tqdm(rawdata.readlines()):
            cur_res = chardet.detect(line)
            result[cur_res['encoding']] += 1

    # If Windows-1252 in input, convert to UTF-8
    print('Detected Encodings:')
    print(tabulate(result.items(), headers=['Encoding', 'Lines']))
    print()
    do_convert = False
    if 'Windows-1252' in result:
        secho('⚠️ Detected Windows-1252 in input, smart quotes will be converted to normal quotes.', fg='yellow')
        do_convert = True

    if do_convert:
        df = pd.read_csv(input_file, encoding='windows-1252')
    else:
        df = pd.read_csv(input_file)

    # Loop through lines and drop brackets
    for i, row in tqdm(df.iterrows(), total=len(df)):
        # Target the text column only
        if 'text' in row.keys():
            text = row['text']
            # If text ends with ], and no [ in line, drop the row
            if text.endswith(']') and '[' not in text:
                df.drop(i, inplace=True)
            elif text.startswith('[') and ']' not in text:
                df.drop(i, inplace=True)
                continue
            # If text contains [ and not ], drop everything after [
            elif '[' in text and ']' not in text:
                df.at[i, 'text'] = text.split('[')[0]
            elif ']' in text and '[' not in text:
                df.at[i, 'text'] = text.split(']')[1]

    # Replace any smart quotes with normal quotes
    df.replace({'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"'}, inplace=True)

    # Print out all symbols in the 'text' column
    ok_symbols = set('"\'.,:!?-') | set(string.ascii_letters) | set(string.digits)
    exclude = set(string.punctuation)
    sym_res = defaultdict(int)

    if 'text' in df.columns:
        text_list = df['text'].tolist()
        for text in tqdm(text_list):  # With Progress
            # Get only symbols
            s_filter = [c for c in text if c in ok_symbols]
            for symbol in s_filter:
                if symbol not in ok_symbols:
                    sym_res[symbol] += 1

    # Print out as table
    if len(sym_res) > 0:
        print('Detected Special Non-Punctuation Symbols:')
        print(tabulate(sym_res.items(), headers=['Symbol', 'Count']))
        print()
        # Ask for confirm
        if not inquirer.confirm('Continue?').execute():
            return

    # Output to UTF 8 csv
    df.to_csv(output_file, index=False, encoding='utf-8', escapechar='\\', doublequote=False)
    secho('✔ CSV exported to ', fg='white', nl=False)
    secho(os.path.basename(output_file), fg='blue')

    # Open output file and remove smart quotes
    if do_convert:
        with yaspin(text='Removing smart quotes', color='yellow') as sp:
            with open(output_file, 'r', encoding='utf-8') as f:
                file_data = f.read()

            new_data = file_data.replace('“', '').replace('”', '').replace('‘', '').replace('’', '')

            with open(output_file, 'w', encoding='utf-8') as new_f:
                new_f.write(new_data)
            sp.ok('✔')

