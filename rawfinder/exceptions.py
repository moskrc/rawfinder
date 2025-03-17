import errno
from pathlib import Path
from typing import Optional

from click import ClickException


class FinderDirectoryDoesNotExistError(Exception):
    """Raised when the specified directory does not exist."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        super().__init__("Directory {} does not exist", str(base_dir))


class FinderNoExtensionError(Exception):
    """Raised when no extensions are specified for the finder."""

    def __init__(self) -> None:
        super().__init__("At least one extension must be specified")


class UnknownReporterError(Exception):
    """Raised when an unsupported reporter type is specified."""

    def __init__(self, reporter_type: str) -> None:
        self.reporter_type = reporter_type
        super().__init__("Reporter type '{}' is not supported", reporter_type)


class DirectoryValidationError(Exception):
    def __init__(self, dir_path: str) -> None:
        super().__init__(f"Directory {dir_path} does not exist")


class UserCancelledError(Exception):
    """Raised when the user cancels the script execution."""

    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message or "User cancelled the script"
        super().__init__(self.message)


class InvalidExceptionFormatError(Exception):
    """Raised when the exception format is invalid."""

    def __init__(self, ext: str, key: str, message: str = "") -> None:
        self.ext = ext
        self.key = key
        super().__init__(message.format(ext, key))


class MissingExtensionsError(ValueError):
    def __init__(self, missing: set[str]) -> None:
        self.missing = missing
        super().__init__(f"Missing extensions for: {missing}")


class OverwriteDisabledError(FileNotFoundError):
    def __init__(self, dest_dir: str) -> None:
        super().__init__(errno.EEXIST, "File {} already exists. Overwrite setting is disabled.", str(dest_dir))


class BooleanValueExpectedError(ClickException):
    def __init__(self, value: str) -> None:
        self.value = value

        super().__init__(f"Boolean value expected (true/false). {value}")


class WriteConfigFileError(ClickException):
    def __init__(self) -> None:
        super().__init__("Error writing config file")


class ChecksumError(ValueError):
    def __init__(self, src: Path, src_hash: str, dst: Path, dst_hash: str) -> None:
        self.src = src
        self.src_hash = src_hash
        self.dst = dst
        self.dst_hash = dst_hash
        super().__init__(f"Checksum mismatch for {src} ({src_hash} != {dst_hash})")
