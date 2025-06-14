import hashlib
import os

from rich.console import Console
from rich.progress import Progress

ignored = []

with open(".thepurgeignore", "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            ignored.append(line)
print(f"Ignored files: {ignored}")


class File(object):
    def __init__(self, file_path, size, file_type):
        self.path = file_path
        self.name = file_path.split("/")[-1]
        self.size = size
        self.file_type = file_type
        self.quick_check_sum = self._quick_check_sum()
        self.full_check_sum = None

    def __repr__(self):
        return f"File(name={self.name}, size={self.size}, file_type={self.file_type})"

    def full_check_sum(self):
        """Calculate the full checksum of the file."""
        if self.full_check_sum is not None:
            return self.full_check_sum
        hasher = hashlib.md5()
        with open(self.name, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        self.full_check_sum = hasher.hexdigest()
        return self.full_check_sum

    def _quick_check_sum(self):
        hasher = hashlib.md5()
        with open(self.path, "rb") as f:
            # Read the first 1024 bytes for a quick checksum
            data = f.read(1024)
            hasher.update(data)
        return hasher.hexdigest()

    def print(self, indent=0, console: Console = Console()):
        """Print file details."""
        indent_str = " " * indent
        console.print(
            f"{indent_str}- [bold yellow]{self.name}[/bold yellow], Size: {self.size}, Quick Checksum: {self.quick_check_sum}"
        )


class Directory(object):
    def __init__(self, path, progress=None):
        self.path = path
        self.name = path.split("/")[-1]
        self.files = []
        self.dirs = []
        self.progress = progress if progress else None
        tasks = self.progress.tasks
        if len(tasks) == 0:
            self.progress.add_task("Loading directory tree", total=None)
        self._load_files()

    def _load_files(self, console: Console = Console()):
        """Load files from the directory."""
        for entry in os.listdir(self.path):
            if self.progress:
                self.progress.advance(0)
            if entry in ignored:
                continue
            self.progress.console.print(f"Processing entry: {self.path}/{entry}")

            full_path = os.path.join(self.path, entry)
            if os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                file_type = entry.split(".")[-1] if "." in entry else "unknown"
                self.files.append(
                    File(file_path=full_path, size=size, file_type=file_type)
                )
            else:
                self.dirs.append(Directory(path=full_path, progress=self.progress))

    def print(self, indent=0, console: Console = Console()):
        """Print directory details."""
        if self.name in ignored:
            return

        indent_str = " " * indent
        console.print(f"{indent_str}[bold cyan]{self.path}[/bold cyan]")
        for file in self.files:
            file.print(indent + 2, console=console)
        for dir in self.dirs:
            dir.print(indent + 2, console=console)
