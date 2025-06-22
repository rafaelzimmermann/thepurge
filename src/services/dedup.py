import os

from multiprocessing import Pool
from models import File, checksum_file
from rich.console import Console
from typing import Callable


def print_duplicates(
    checksum_files: dict[str, list[File]], console: Console = Console()
):
    for checksum, files in checksum_files.items():
        if len(files) > 1:
            console.print(
                f"[bold red]Duplicate files found with checksum {checksum}:[/bold red]"
            )
            for file in files:
                console.print(f"  - {file.path}")
    console.print("[bold green]Checksum analysis complete.[/bold green]")


class Deduplicator:

    def __init__(self, files: list[File], strategy: Callable[[dict[str, list[File]]], bool] = print_duplicates, console: Console = Console()):
        self.console = console
        self.files = files
        self.checksum_files = self._checksums()
        self.strategy = strategy
    
    def _checksums(self) -> list[str]:
        files = [file.path for file in self.files]
        with Pool(processes=os.cpu_count() * 2) as pool:
            return pool.map(checksum_file, files)

    def deduplicate(self) -> bool:
        checksum_files = {}
        for file, checksum in zip(self.files, self.checksum_files):
            if checksum not in checksum_files:
                checksum_files[checksum] = []
            checksum_files[checksum].append(file)
        non_duplicated = []
        for checksum in checksum_files:
            if len(checksum_files[checksum]) <= 1:
                non_duplicated.append(checksum)
        for checksum in non_duplicated:
            del checksum_files[checksum]
        return self.strategy(checksum_files)
