import hashlib
import os

from rich.console import Console
from multiprocessing import Pool


def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def get_block_size(path):
    stat = os.statvfs(path)
    return stat.f_bsize


def checksum_file(file_path: str) -> str:
    hasher = hashlib.md5()
    block_size = get_block_size(file_path)
    buffer_size = block_size * 1024
    size = os.path.getsize(file_path)

    print(
        f"Calculating checksum {file_path} (block size: {block_size}), file size: {sizeof_fmt(size)}"
    )
    with open(file_path, "rb") as f:
        pos = 0
        while pos < size:
            chunk = f.read(buffer_size)
            hasher.update(chunk)
            pos += len(chunk)

    return hasher.hexdigest()


class File(object):
    def __init__(self, file_path, size, file_type):
        self.path = file_path
        self.name = file_path.split("/")[-1]
        self.size = size
        self.file_type = file_type
        self.quick_check_sum = self._quick_check_sum()
        self._full_check_sum = None

    def __repr__(self):
        return f"File(name={self.name}, size={self.size}, file_type={self.file_type})"

    def full_check_sum(self):
        """Calculate the full checksum of the file."""
        if self._full_check_sum is not None:
            return self._full_check_sum
        self._full_check_sum = checksum_file(self.path)
        return self._full_check_sum

    def _quick_check_sum(self):
        file_size = os.stat(self.path).st_size
        return f"{file_size}_{self.file_type}"

    def print(self, indent=0, console: Console = None):
        """Print file details."""
        indent_str = " " * indent
        _p = console.print if console else print
        _p(
            f"{indent_str}- [bold yellow]{self.name}[/bold yellow], Size: {self.size}, Quick Checksum: {self.quick_check_sum}"
        )


class Directory(object):
    def __init__(self, path, files_extensions: set[str] = None):
        self.path = path
        self.name = path.split("/")[-1]
        self.files = []
        self.dirs = []
        self.files_extensions = files_extensions if files_extensions else set([])

    def print(self, indent: int = 0, console: Console = None):
        """Print directory details."""
        indent_str = " " * indent
        _p = console.print if console else print
        _p(f"{indent_str}{self.path}")
        for file in self.files:
            file.print(indent + 2, console=console)
        for dir in self.dirs:
            dir.print(indent + 2, console=console)

    def recursive_list(self, files: list[File] = []) -> list[File]:
        files.extend(self.files)
        for dir in self.dirs:
            dir.recursive_list(files)
        return files


if __name__ == "__main__":
    import sys

    files = sys.argv[1:]
    for file in files:
        print(checksum_file(file))
