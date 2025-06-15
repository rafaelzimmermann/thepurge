import hashlib
import os

from multiprocessing import Pool


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

    def print(self, indent=0):
        """Print file details."""
        indent_str = " " * indent
        print(
            f"{indent_str}- [bold yellow]{self.name}[/bold yellow], Size: {self.size}, Quick Checksum: {self.quick_check_sum}"
        )


class Directory(object):
    def __init__(self, path, files_extensions: set[str] = None):
        self.path = path
        self.name = path.split("/")[-1]
        self.files = []
        self.dirs = []
        self.files_extensions = files_extensions if files_extensions else set([])

    def print(self, indent: int = 0):
        """Print directory details."""
        indent_str = " " * indent
        print(f"{indent_str}{self.path}")
        for file in self.files:
            file.print(indent + 2)
        for dir in self.dirs:
            dir.print(indent + 2)
