import sys

from models import Directory
from rich.console import Console
from rich.progress import Progress


def load_checksum_files(dir: Directory, checksum_files: dict = {}, console: Console = Console()) -> dict[str, list[str]]:
    for file in dir.files:
        if file.quick_check_sum not in checksum_files:
            checksum_files[file.quick_check_sum] = []
        checksum_files[file.quick_check_sum].append(file)
    for dir in dir.dirs:
        load_checksum_files(dir, checksum_files, console)
    return checksum_files

def main(folder_path: str = "."):
    with Progress() as progress:
        dir = Directory(folder_path, progress=progress)
    dir.print(console=Console())

    checksum_files = load_checksum_files(dir)
    console = Console()
    for checksum, files in checksum_files.items():
        if len(files) > 1:
            console.print(f"[bold red]Duplicate files found with checksum {checksum}:[/bold red]")
            for file in files:
                console.print(f"  - {file.path}")
    console.print("[bold green]Checksum analysis complete.[/bold green]")

if __name__ == "__main__":
    import sys

    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    main(folder_path=folder_path)
