# Concat Operations for combining CSV files
from InquirerPy import inquirer
from click import secho
import pandas as pd
import os
from glob import glob
from yaspin import yaspin


def sorted_by_time(files: list[str]) -> list[str]:
    """
    Sort a list of files by creation time

    :param files: list of files to sort
    :return: list of (filename, created_time) tuples
    """
    # Read all CSV files in directory into a list of tuples (filename, created_time)
    result = [(f, os.path.getctime(f)) for f in files]
    # Sort the list by the created time
    result.sort(key=lambda x: x[1])
    # Discard the created time
    return [f for f, _ in result]


def read_csv(files: list[str]) -> pd.DataFrame:
    """
    Read CSV files into a dataframe

    :param files: list of files to read
    :return: dataframe
    """
    with yaspin(text="Reading CSV files...", color='yellow') as sp:
        result = pd.concat([pd.read_csv(f) for f in files])
        sp.ok("✔ ")
    return result


def concat_csv(input_dir: str = None, output_file: str = None) -> None:
    """
    Concatenate CSV files in a directory
    """
    if not input_dir:  # Set default input directory
        input_dir = os.getcwd()

    if not output_file:  # Set default output file
        output_file = os.path.join(input_dir, "concat.csv")

    # Read all CSV files into sorted list
    csv_files = sorted_by_time(glob(input_dir + "/*.csv"))

    if not len(csv_files) >= 2:
        secho("❌ ", fg='red', nl=False)
        secho("Error: Need 2+ CSV files to concatenate. Found ", nl=False)
        secho(str(len(csv_files)), fg='red', nl=False)
        secho(" files in ", nl=False)
        secho(f'[{input_dir}]', fg='blue')
        return

    with yaspin(text="Reading CSV files...", color='yellow') as sp:
        df = pd.read_csv(csv_files[0])
        for filename in csv_files[1:]:
            df = pd.concat([df, pd.read_csv(filename)])
        sp.ok("✔ ")

    secho(f"{len(df)} rows read from {len(csv_files)} files", fg='green')
    secho("Outputting file to: ", nl=False)
    secho(f'[{output_file}]', fg='blue')

    confirm = inquirer.confirm(
        message="Proceed?",
        default=True,
        confirm_letter="Y",
        reject_letter="n",
    ).execute()
    if not confirm:
        return
    with yaspin(text="Writing CSV file...", color='yellow') as sp:
        df.to_csv(output_file, escapechar='\\', doublequote=False, index=False, index_label=False)
        sp.ok("✔ ")
