import sys

from models import Directory
from rich.console import Console
from rich.progress import Progress


def main(folder_path: str = "."):
    with Progress() as progress:
        dir = Directory(folder_path, progress=progress)
    dir.print(console=Console())


if __name__ == "__main__":
    import sys

    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    main(folder_path=folder_path)
