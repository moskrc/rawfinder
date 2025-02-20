import asyncio
import logging
from pathlib import Path
from typing import ClassVar, Optional

from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeElapsedColumn

from rawfinder.copier import AsyncFileCopier
from rawfinder.finder import FileFinder
from rawfinder.matcher import FileMatcher


class AsyncRawFinderApp:
    JPEG_EXTENSIONS: ClassVar[set[str]] = {".jpeg", ".jpg"}
    RAW_EXTENSIONS: ClassVar[set[str]] = {
        ".3fr",
        ".ari",
        ".arw",
        ".srf",
        ".sr2",
        ".bay",
        ".braw",
        ".cri",
        ".crw",
        ".cr2",
        ".cr3",
        ".cap",
        ".iiq",
        ".eip",
        ".dcs",
        ".dcr",
        ".drf",
        ".k25",
        ".kdc",
        ".dng",
        ".erf",
        ".fff",
        ".gpr",
        ".mef",
        ".mdc",
        ".mos",
        ".mrw",
        ".nef",
        ".nrw",
        ".orf",
        ".pef",
        ".ptx",
        ".pxn",
        ".r3d",
        ".raf",
        ".raw",
        ".rw2",
        ".rwl",
        ".rwz",
        ".srw",
        ".tco",
        ".x3f",
    }

    def __init__(self, jpeg_dir: Path, raw_dir: Path, dest_dir: Path, logger: Optional[logging.Logger] = None):
        self.jpeg_dir = jpeg_dir
        self.raw_dir = raw_dir
        self.dest_dir = dest_dir
        self.logger = logger or logging.getLogger(__name__)

        self.jpeg_finder = FileFinder(jpeg_dir, self.JPEG_EXTENSIONS)
        self.raw_finder = FileFinder(raw_dir, self.RAW_EXTENSIONS)
        self.copier = AsyncFileCopier()

    async def run(self) -> None:
        self.logger.info(f"Find JPEG files in '{self.jpeg_dir}'...")
        jpeg_files = self.jpeg_finder.find_files()
        self.logger.info(f"Found {len(jpeg_files)} JPEG files.")

        self.logger.info(f"Find RAW files in '{self.raw_dir}'...")
        raw_files = self.raw_finder.find_files()
        self.logger.info(f"Found {len(raw_files)} RAW files.")

        matcher = FileMatcher(raw_files)
        matches = []
        for jpeg in jpeg_files:
            raw = matcher.get_matching_raw(jpeg)
            if raw:
                matches.append((jpeg, raw))
            else:
                self.logger.warning(f"RAW file not found for '{jpeg}'.")

        total = len(matches)
        self.logger.info(f"Found {total} matching JPEG-RAW files.")

        confirm = input("Do you want to copy these files? [Y/n] ")
        if confirm.lower() not in ("y", ""):
            self.logger.info("Copying files canceled.")
            return

        progress = Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )

        with progress:
            task_id = progress.add_task(f"Copying files from {self.raw_dir} to {self.dest_dir}", total=total)

            async def copy_and_update(raw_file_path: Path) -> None:
                await self.copier.copy(raw_file_path, self.dest_dir)
                progress.advance(task_id)

            await asyncio.gather(*(copy_and_update(raw_file_path) for _, raw_file_path in matches))

        self.logger.info(f"Finished copying {total} files to '{self.dest_dir}'.")
