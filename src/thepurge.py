import os
import sys

import questionary
import typer
from rich.console import Console
from rich.progress import Progress
from rich.prompt import Confirm
from typing_extensions import Annotated

from models import Directory, File
from service import delete_duplicates, move_duplicates, print_duplicates

MOVE = "MOVE"
PRINT = "PRINT"
DELETE = "DELETE"
strategies = [PRINT, MOVE, DELETE]


def load_checksum_files(
    dir: Directory, checksum_files: dict = {}, console: Console = Console()
) -> dict[str, list[File]]:
    for file in dir.files:
        if file.quick_check_sum not in checksum_files:
            checksum_files[file.quick_check_sum] = []
        checksum_files[file.quick_check_sum].append(file)
    for dir in dir.dirs:
        load_checksum_files(dir, checksum_files, console)

    return checksum_files


def the_purge(folder_path: str = ".", extensions: set[str] = None):
    selected_strategy = questionary.select(
        "Select a strategy for handling duplicate files:",
        choices=strategies,
        default=PRINT,
    ).ask()
    if selected_strategy not in strategies:
        print(f"Invalid strategy selected: {selected_strategy}")
        sys.exit(1)

    with Progress() as progress:
        dir = Directory(folder_path, files_extensions=extensions)
    dir.print()

    checksum_files = load_checksum_files(dir)
    console = Console()

    if selected_strategy == MOVE and Confirm.ask("Do you want to move duplicates?"):
        move_duplicates(checksum_files, console)
    elif selected_strategy == PRINT:
        print_duplicates(checksum_files, console)
    elif selected_strategy == DELETE and Confirm.ask(
        "Do you want to delete duplicates?"
    ):
        delete_duplicates(checksum_files, console)
    else:
        sys.exit(1)


def main(
    folder_path: Annotated[
        str, typer.Argument(help="The folder to performe duplicated purge")
    ] = ".",
    extensions: Annotated[
        str,
        typer.Argument(
            help="Only target files with provided extensions. Example: jpg,png,gif"
        ),
    ] = None,
):
    extensions = extensions.split(",") if extensions is not None else []
    the_purge(folder_path=folder_path, extensions=set(extensions))


if __name__ == "__main__":
    typer.run(main)
