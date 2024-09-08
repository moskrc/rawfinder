import pathlib


class FileStorage:
    def __init__(self):
        """Initializes an empty storage dictionary and a flag to track if indexing is complete."""

        self.indexed = False
        self._storage: dict[str, pathlib.Path] = {}

    def make_index(self, files: list[pathlib.Path]):
        """Populates the internal storage with the provided list of file paths.
        Each file's stem (filename without extension) is converted to lowercase
        and used as a key, while the full path is stored as the value.
        """
        for file in files:
            self._storage[file.stem.lower()] = file

        # Mark the storage as indexed
        self.indexed = True

    def get(self, file_name: str):
        """Retrieves a file path by its name, ignoring case."""

        if not self.indexed:
            raise ValueError("FileStorage has not been indexed yet")

        return self._storage.get(file_name.lower())
