import os
import sys

import typer
from rich.console import Console
from typing_extensions import Annotated

from models import Directory, File
from services.dedup import (
    Deduplicator,
    print_duplicates,
    write_to_csv
)
from services.treeloader import build_tree

MOVE = "MOVE"
PRINT = "PRINT"
CSV = "CSV"
DELETE = "DELETE"

strategies = {
    PRINT: print_duplicates,
    CSV: write_to_csv
}


def the_purge(folder_path: str = ".", extensions: set[str] = None, strategy: str = PRINT, processes: int = 1):
    selected_strategy = PRINT
    if selected_strategy not in strategies:
        print(f"Invalid strategy selected: {selected_strategy}")
        sys.exit(1)

    dir = build_tree(Directory(folder_path, files_extensions=extensions))
    dir.print(console=Console())
    deduplicator = Deduplicator(dir.recursive_list(), strategy=strategies[strategy.upper()], processes=processes)
    deduplicator.deduplicate()

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
    strategy: Annotated[
        str,
        typer.Option(
            help="Deduplicate strategy. print, csv."
        ),
    ] = PRINT,
    processes: Annotated[
        int,
        typer.Option(
            help="Number of processes."
        ),
    ] = 1
):
    extensions = extensions.split(",") if extensions is not None else []
    the_purge(folder_path=folder_path, extensions=set(extensions), strategy=strategy, processes=processes)


if __name__ == "__main__":
    typer.run(main)
