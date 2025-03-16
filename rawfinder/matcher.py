from collections import defaultdict
from pathlib import Path
from typing import Optional


class FileMatcher:
    def __init__(self, source_files: list[Path]):
        self.source_files = source_files
        self._index: dict[str, Path] = defaultdict()

    def _index_sources(self) -> None:
        for source_file in self.source_files:
            self._index[source_file.stem.lower()] = source_file

    def get_matching_source(self, photo_file: Path) -> Optional[Path]:
        if not self._index:
            self._index_sources()
        return self._index.get(photo_file.stem.lower())
