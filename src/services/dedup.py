import os
import sys
import questionary

from models import File
from rich.console import Console
from rich.progress import track


def compare(files: list[File]) -> bool:
    first = files[0]
    checksum = first.full_check_sum
    for file in files[1:]:
        if file.full_check_sum != checksum:
            return False
    return True


def print_duplicates(
    checksum_files: dict[str, list[File]], console: Console = Console()
):
    for checksum, files in checksum_files.items():
        if len(files) > 1:
            if not compare(files):
                console.print(
                    f"[bold red]Checksum mismatch for files with checksum {checksum}. Skipping...[/bold red]"
                )
                for file in files:
                    console.print(f"  - {file.path} {file.full_check_sum()}")
                continue
            console.print(
                f"[bold red]Duplicate files found with checksum {checksum}:[/bold red]"
            )
            for file in files:
                console.print(f"  - {file.path}")
    console.print("[bold green]Checksum analysis complete.[/bold green]")


def move_duplicates(
    checksum_files: dict[str, list[File]],
    target_directory: str,
    console: Console = Console(),
):
    print(
        "You selected the MOVE strategy. This will move duplicate files to a specified directory."
    )
    target_directory = questionary.text(
        "Enter the target directory to move duplicates to:", default="duplicates"
    ).ask()
    if not target_directory:
        print("No target directory specified. Exiting.")
        sys.exit(1)
    if not os.path.exists(target_directory):
        raise FileNotFoundError(
            f"Target directory '{target_directory}' does not exist."
        )
    if len(os.path.lisdir(target_directory)) > 0:
        console.print(
            f"[bold yellow]Warning: Target directory '{target_directory}' is not empty. Duplicates will be moved here.[/bold yellow]"
        )
        raise Exception(
            f"Target directory '{target_directory}' is not empty. Please choose an empty directory or clear it before proceeding."
        )

    for checksum, files in track(
        checksum_files.items(), description="Moving duplicate files..."
    ):
        if len(files) > 1:
            if not compare(files):
                console.print(
                    f"[bold red]Checksum mismatch for files with checksum {checksum}. Skipping...[/bold red]"
                )
                continue
            sorted_files = sorted(files, key=lambda f: f.name, reverse=False)
            move_files = sorted_files[1:]  # Keep the first file, move the rest
            console.print(
                f"[bold red]Moving duplicate files with checksum {checksum} to {target_directory}:[/bold red]"
            )
            for file in move_files:
                target_path = os.path.join(target_directory, file.path)
                target_path_dir = os.path.dirname(target_path)
                if not os.path.exists(target_path_dir):
                    os.makedirs(target_path_dir)
                try:
                    os.rename(file.path, target_path)
                    console.print(f"  - Moved {file.path} to {target_path}")
                except Exception as e:
                    console.print(f"[bold red]Error moving {file.path}: {e}[/bold red]")
    console.print("[bold green]Duplicate files moved successfully.[/bold green]")


def delete_duplicates(
    checksum_files: dict[str, list[File]], console: Console = Console()
):
    for checksum, files in track(
        checksum_files.items(), description="Deleting duplicate files..."
    ):
        if len(files) > 1:
            if not compare(files):
                console.print(
                    f"[bold red]Checksum mismatch for files with checksum {checksum}. Skipping...[/bold red]"
                )
                continue
            sorted_files = sorted(files, key=lambda f: f.name, reverse=False)
            delete_files = sorted_files[1:]  # Keep the first file, delete the rest
            console.print(
                f"[bold red]Deleting duplicate files with checksum {checksum}:[/bold red]"
            )
            for file in delete_files:
                try:
                    os.remove(file.path)
                    console.print(f"  - Deleted {file.path}")
                except Exception as e:
                    console.print(
                        f"[bold red]Error deleting {file.path}: {e}[/bold red]"
                    )
    console.print("[bold green]Duplicate files deleted successfully.[/bold green]")
