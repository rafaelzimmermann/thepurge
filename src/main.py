import os
import sys
import questionary

from models import Directory, File
from service import print_duplicates, move_duplicates, delete_duplicates
from rich.console import Console
from rich.progress import Progress

strategies = ["MOVE", "PRINT", "DELETE"]


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


def main(folder_path: str = "."):
    selected_strategy = questionary.select(
        "Select a strategy for handling duplicate files:",
        choices=strategies,
        default="MOVE",
    ).ask()
    if selected_strategy not in strategies:
        print(f"Invalid strategy selected: {selected_strategy}")
        sys.exit(1)

    with Progress() as progress:
        dir = Directory(folder_path, progress=progress)
    dir.print(console=Console())

    checksum_files = load_checksum_files(dir)
    console = Console()

    if selected_strategy == "MOVE":
        move_duplicates(checksum_files, console)
    elif selected_strategy == "PRINT":
        print_duplicates(checksum_files, console)
    elif selected_strategy == "DELETE":
        delete_duplicates(checksum_files, console)
    else:
        console.print(
            f"[bold red]Unknown strategy selected: {selected_strategy}[/bold red]"
        )
        sys.exit(1)


if __name__ == "__main__":
    import sys

    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    main(folder_path=folder_path)
