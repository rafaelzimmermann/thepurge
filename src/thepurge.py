import os
import sys

import typer
from rich.console import Console
from typing_extensions import Annotated

from models import Directory, File
from services.dedup import Deduplicator, print_duplicates, write_to_csv, move_duplicates
from services.treeloader import build_tree

MOVE = "MOVE"
PRINT = "PRINT"
CSV = "CSV"
DELETE = "DELETE"

strategies = {PRINT: print_duplicates, CSV: write_to_csv, MOVE: move_duplicates}


def the_purge(
    folder_path: str = ".",
    extensions: set[str] = None,
    strategy: str = PRINT,
    processes: int = 1,
    destination_dir: str = None,
):
    if strategy not in strategies:
        print(f"Invalid strategy selected: {strategy}")
        sys.exit(1)

    strategy_func = strategies[strategy]

    if strategy == MOVE:
        if (
            destination_dir is None
            or not os.path.exists(destination_dir)
            or not os.path.isdir(destination_dir)
        ):
            print("destintation_dir must be provided.")
            sys.exit(2)
        strategy_func = strategy_func(destination_dir)

    dir = build_tree(Directory(folder_path, files_extensions=extensions))
    dir.print(console=Console())
    deduplicator = Deduplicator(
        dir.recursive_list(), strategy=strategy_func, processes=processes
    )
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
        typer.Option(help="Deduplicate strategy. print, csv."),
    ] = PRINT,
    destination_dir: Annotated[
        str,
        typer.Option(help="Destination directory used to move deplicated files"),
    ] = None,
    processes: Annotated[
        int,
        typer.Option(help="Number of processes."),
    ] = 1,
):
    extensions = extensions.split(",") if extensions is not None else []
    the_purge(
        folder_path=folder_path,
        extensions=set(extensions),
        strategy=strategy.upper(),
        processes=processes,
        destination_dir=destination_dir,
    )


if __name__ == "__main__":
    typer.run(main)
