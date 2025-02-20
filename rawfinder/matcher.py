from pathlib import Path


class FileMatcher:
    def __init__(self, raw_files: list[Path]):
        self.index: dict[str, Path] = {}
        self.build_index(raw_files)

    def build_index(self, raw_files: list[Path]) -> None:
        """
        Index RAW files by their names. The key is the lowercase name of the file without extension.
        :param raw_files:
        :return: None
        """
        for raw in raw_files:
            key = raw.stem.lower()
            if key not in self.index:
                self.index[key] = raw

    def get_matching_raw(self, jpeg_file: Path) -> Path | None:
        """
        Get matching RAW file for JPEG file.
        :param jpeg_file:
        :return: matching RAW file or None
        """
        return self.index.get(jpeg_file.stem.lower())
