import pathlib


class FileStorage:
    def __init__(self):
        self.indexed = False
        self._storage: dict[str, pathlib.Path] = dict()

    def make_index(self, files: list[pathlib.Path]):
        for file in files:
            self._storage[file.stem.lower()] = file

        self.indexed = True

    def get(self, file_name: str):
        if not self.indexed:
            raise ValueError("not indexed")

        return self._storage.get(file_name.lower())
