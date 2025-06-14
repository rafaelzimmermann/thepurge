import os


class DirectoryService:

    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    def list_files(self):
        """List all files in the directory."""
        return os.listdir(self.directory_path)
