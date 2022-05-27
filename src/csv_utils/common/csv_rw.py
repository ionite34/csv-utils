# CSV Read Write Utilities
from __future__ import annotations

import os
from InquirerPy import inquirer


def get_csvs(folder: str) -> dict[str, str]:
    # Show current directory's csvs
    csvs = {}  # Map of csv_name | csv_path
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            csvs[file] = os.path.join(folder, file)
    return csvs


def select_input(folder: str = None) -> str | None:
    if not folder:  # Set default input directory
        folder = os.getcwd()
    csvs = get_csvs(folder)

    if not csvs:
        print("No csvs found in directory")
        return None

    selected_f = inquirer.select(
        message="Select input file:",
        choices=list(csvs.keys()),
        max_height="80%",
    ).execute()

    return csvs.get(selected_f)


def select_output(default: str) -> str:
    out_path = inquirer.filepath(
        message="Select output file:",
        default=default,
        only_files=True,
    ).execute()
    return out_path
