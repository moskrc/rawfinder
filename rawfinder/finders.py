import pathlib
import typing
from functools import lru_cache


class BaseFinder:
    extensions: typing.ClassVar[list[str]] = []

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path

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

    def find(self) -> list[pathlib.Path]:
        return [
            file
            for ext in self.extensions
            for file in pathlib.Path(self.path).glob(
                BaseFinder._convert_to_case_insensitive(ext),
            )
        ]

    def __str__(self) -> str:
        return str(self.path)


class JpegFinder(BaseFinder):
    extensions: typing.ClassVar[list[str]] = [".jpeg", ".jpg"]


class RawFinder(BaseFinder):
    extensions: typing.ClassVar[list[str]] = [
        ".3fr",  # Hasselblad
        ".ari",  # Arri Alexa
        ".arw",
        ".srf",
        ".sr2",  # Sony
        ".bay",  # Casio
        ".braw",  # Blackmagic Design
        ".cri",  # Cintel
        ".crw",
        ".cr2",
        ".cr3",  # Canon
        ".cap",
        ".iiq",
        ".eip",  # Phase One
        ".dcs",
        ".dcr",
        ".drf",
        ".k25",
        ".kdc",  # Kodak
        ".dng",  # Adobe
        ".erf",  # Epson
        ".fff",  # Imacon/Hasselblad raw
        ".gpr",  # GoPro
        ".mef",  # Mamiya
        ".mdc",  # Minolta, Agfa
        ".mos",  # Leaf
        ".mrw",  # Minolta, Konica Minolta
        ".nef",
        ".nrw",  # Nikon
        ".orf",  # Olympus
        ".pef",
        ".ptx",  # Pentax
        ".pxn",  # Logitech
        ".R3D",  # RED Digital Cinema
        ".raf",  # Fuji
        ".raw",
        ".rw2",  # Panasonic
        ".raw",
        ".rwl",
        ".dng",  # Leica
        ".rwz",  # Rawzor
        ".srw",  # Samsung
        ".tco",  # intoPIX
        ".x3f",  # Sigma
    ]
