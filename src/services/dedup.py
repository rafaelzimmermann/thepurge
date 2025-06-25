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


def write_to_csv(checksum_files: dict[str, list[File]], console: Console = Console()):
    with open("duplicates.csv", "w") as _out:
        _out.write("checksum,path,size\n")
        for checksum, files in checksum_files.items():
            if len(files) <= 1:
                continue
            for file in files:
                _out.write(f'{checksum},"{file.path}",{file.size}\n')


def move_duplicates(target_dir):
    def move_func(checksum_files: dict[str, list[File]], console: Console = Console()):
        for checksum, files in checksum_files.items():
            if len(files) <= 1:
                continue
            for _f in files:
                if not os.path.exists(_f.path):
                    console.print(f"[bold red]Skipping due to missing file: {_f.path}")
                    continue
            keep = files[:1][0]
            console.print(f"[bold green]Keeping: {keep.path}[/bold green]")
            move = files[1:]
            index = 0
            for _f in move:
                new_file_name = f"{checksum}_{index}_{_f.name}"
                new_path = os.path.join(target_dir, new_file_name)
                console.print(f"[bold red]Moving {_f.path} -> {new_path}[/bold red]")
                os.rename(_f.path, new_path)
                index += 1

    return move_func


class Deduplicator:

    def __init__(
        self,
        files: list[File],
        processes: int = 1,
        strategy: Callable[[dict[str, list[File]]], bool] = print_duplicates,
        console: Console = Console(),
    ):
        self.console = console
        self.files = files
        self.processes = processes
        self.checksum_files = self._checksums()
        self.strategy = strategy

    def _checksums(self) -> list[str]:
        files = [file.path for file in self.files]
        with Pool(processes=self.processes) as pool:
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
