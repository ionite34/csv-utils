# Command Entry Point
from .concat import concat_csv
from click import secho
from InquirerPy.base.control import Choice
from InquirerPy import inquirer


def cli() -> None:
    # Entry point
    secho("Welcome to CSV-Utils v0.1.0", fg="yellow")
    action = inquirer.select(
        message="Select Action:",
        choices=[
            "Concat CSV Files",
            Choice(value=None, name="Exit"),
        ],
        default=0,
    ).execute()
    if action == "Concat CSV Files":
        concat()


def concat(input_dir=None, output_file=None):
    """
    Concatenate all CSV files in a directory into a single CSV file.
    """
    concat_csv(input_dir, output_file)
