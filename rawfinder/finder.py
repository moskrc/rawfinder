from pathlib import Path


class FileFinder:
    def __init__(self, base_dir: Path, extensions: set[str]):
        self.base_dir = base_dir
        self.extensions = {ext.lower() for ext in extensions}

    def find_files(self) -> list[Path]:
        """
        Find files in base_dir with extensions
        :return: list of Path objects
        """

        return [path for path in self.base_dir.rglob("*") if path.is_file() and path.suffix.lower() in self.extensions]
