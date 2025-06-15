import os

from multiprocessing import Pool
from models import File, Directory

ignored = []

with open(".thepurgeignore", "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            ignored.append(line)
print(f"Ignored files: {ignored}")


def _load_file(full_path: str, entry: str) -> File | None:
    try:
        size = os.path.getsize(full_path)
        file_type = entry.split(".")[-1] if "." in entry else "unknown"
        return File(file_path=full_path, size=size, file_type=file_type)
    except OSError as e:
        print(f"Error reading file {full_path}: {e}")
        return None


def _load_dir(full_path: str, entry: str, files_extensions: set[str] = None):
    return Directory(path=full_path, files_extensions=files_extensions)


def _ignored_file(entry: str) -> bool:
    """Check if the file should be ignored."""
    return entry in ignored


def _file_extension(filename: str) -> str | None:
    """Get the file extension."""
    return filename.split(".")[-1].lower() if "." in filename else None

def _skip_file(entry: str, files_extensions: set[str]) -> bool:
    """Check if the file should be skipped based on its extension."""
    if not files_extensions:
        return False
    ext = _file_extension(entry)
    return ext is None or ext not in files_extensions

def build_tree(directory: Directory) -> Directory:
    """Load files from the directory."""
    files = []
    dirs = []
    for entry in os.listdir(directory.path):
        if _ignored_file(entry):
            continue
        full_path = os.path.join(directory.path, entry)
        is_file = os.path.isfile(full_path)
        if is_file:
            if _skip_file(entry, directory.files_extensions):
                print(f"Skipping {entry}")
                continue
           
            print(f"Processing entry: {full_path}")
            files.append((full_path, entry))
        else:
            dirs.append(Directory(full_path, directory.files_extensions))
    with Pool() as pool:
        directory.files = pool.starmap(_load_file, files)
    directory.dirs = [build_tree(dir) for dir in dirs]
    return directory
