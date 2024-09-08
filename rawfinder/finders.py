import abc
import pathlib
from functools import lru_cache


class BaseFinder(abc.ABC):
    extensions: list[str] = []

    def __init__(self, path: str) -> None:
        self.path = pathlib.Path(path)

    @classmethod
    @lru_cache
    def _convert_to_case_insensitive(cls, extension: str) -> str:
        """
        The case_sensitive param for glob/rglob was added in Python 3.12
        this method allow emulation of case_sensitive for older versions
        of Python
        """
        ext = "".join(f"[{c.lower()}{c.upper()}]" for c in extension[1:])
        return f"*{extension[0]}{ext}"

    @lru_cache
    def find(self) -> list[pathlib.Path]:
        return [
            file
            for ext in self.extensions
            for file in pathlib.Path(self.path).glob(
                BaseFinder._convert_to_case_insensitive(ext),
            )
        ]

    def __str__(self):
        return str(self.path)


class JpegFinder(BaseFinder):
    extensions = [".jpeg", ".jpg"]


class RawFinder(BaseFinder):
    extensions = [
        ".cr2",
        ".nef",
        ".dng",
        ".arw",
        ".raf",
        ".rw2",
        ".orf",
        ".srw",
        ".pef",
        ".x3f",
        ".sr2",
    ]
