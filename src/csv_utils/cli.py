# Command Entry Point
from .concat import concat_csv
from .convert import convert_csv
from click import secho
from InquirerPy.base.control import Choice
from InquirerPy import inquirer
from bs4 import UnicodeDammit


def cli() -> None:
    # Entry point
    secho("Welcome to CSV-Utils v0.1.0", fg="yellow")
    action = inquirer.select(
        message="Select Action:",
        choices=[
            Choice(value='Concat', name="Concat | Combined multiple CSV Files"),
            Choice(value='Convert', name="Convert | Convert CSV Formats such as Encoding, Escapes and Delimiters."),
            Choice(value=None, name="Exit"),
        ],
        default=0,
    ).execute()
    if action == 'Concat':
        concat_csv()
    elif action == 'Convert':
        convert_csv()
