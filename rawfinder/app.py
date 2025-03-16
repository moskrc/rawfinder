import logging
from pathlib import Path
from typing import Optional

from rawfinder.copier import FileCopier
from rawfinder.exceptions import ChecksumError, DirectoryValidationError, OverwriteDisabledError, UserCancelledError
from rawfinder.finder import FileFinder
from rawfinder.matcher import FileMatcher
from rawfinder.reporters import ProgressReporter

logger = logging.getLogger(__name__)


class RawFinderApp:
    def __init__(
        self,
        photos_dir: Path,
        sources_dir: Path,
        dest_dir: Path,
        copier: FileCopier,
        progress_reporter: ProgressReporter,
        dry_run: bool = False,
        photo_extensions: Optional[list[str]] = None,
        source_extensions: Optional[list[str]] = None,
    ) -> None:
        if source_extensions is None:
            source_extensions = []
        if photo_extensions is None:
            photo_extensions = []
        self.photos_dir = photos_dir
        self.sources_dir = sources_dir
        self.dest_dir = dest_dir
        self.copier = copier
        self.progress_reporter = progress_reporter
        self.dry_run = dry_run
        self.photo_extensions = photo_extensions
        self.source_extensions = source_extensions
        self._validate_directories()

    def _validate_directories(self) -> None:
        for dir_path in [self.photos_dir, self.sources_dir]:
            if not dir_path.is_dir():
                raise DirectoryValidationError(str(dir_path))

    def _find_photo_files(self) -> list[Path]:
        finder = FileFinder(self.photos_dir, set(self.photo_extensions))
        files = finder.find_files()
        logger.info(f"Found {len(files)} photo files in '{self.photos_dir}'")
        return files

    def _find_source_files(self) -> list[Path]:
        finder = FileFinder(self.sources_dir, set(self.source_extensions))
        files = finder.find_files()
        logger.info(f"Found {len(files)} source files in '{self.sources_dir}'")
        return files

    def _match_files(self, photo_files: list[Path], source_files: list[Path]) -> list[tuple[Path, Path]]:
        matcher = FileMatcher(source_files)
        matches = []
        for photo_file in photo_files:
            if source := matcher.get_matching_source(photo_file):
                matches.append((photo_file, source))
            else:
                logger.warning(f"No source match for '{photo_file.name}'")
        return matches

    def _confirm_create_dest_dir(self) -> bool:
        confirm = input(f"Directory '{self.dest_dir}' does not exist. Create it? [Y/n] ")
        return confirm.lower() in ("", "y")

    def _confirm_copy(self, matches: list) -> bool:
        if not matches:
            logger.info("Nothing to copy")
            return False

        if self.dry_run:
            logger.info(f"Dry-run: Would copy {len(matches)} files")
            return True

        confirm = input(f"Copy {len(matches)} files to {self.dest_dir}? [Y/n] ")
        return confirm.lower() in ("", "y")

    def _handle_results(self, results: list[bool]) -> None:
        success_count = sum(1 for r in results if r is True)
        error_count = len(results) - success_count

        logger.info(f"Successfully processed: {success_count} files")
        if error_count > 0:
            logger.warning(f"Failed processing: {error_count} files")

    def _copy_files(self, matches: list[tuple[Path, Path]]) -> None:
        self.progress_reporter.start(len(matches), "Copying RAW files")

        try:
            results = []
            for _, raw_path in matches:
                result = self._process_file(raw_path)
                results.append(result)

            self._handle_results(results)

        finally:
            self.progress_reporter.complete()

    def _process_file(self, raw_path: Path) -> bool:
        try:
            success = self.copier.copy(raw_path, self.dest_dir)
            description = "copied" if success else "failed"
        except ChecksumError as e:
            logger.warning(f"Failed to copy '{raw_path}': {e}")
            description = "failed (checksum mismatch)"
            success = False
        except OverwriteDisabledError:
            logger.warning(f"File '{raw_path}' already exists")
            description = "skipped (overwrite disabled)"
            success = False
        except OSError as e:
            description = "failed"
            success = False
            logger.warning(e)

        self.progress_reporter.update(raw_path.name, success, description)
        return success

    def run(self) -> None:
        photo_files = self._find_photo_files()
        source_files = self._find_source_files()
        matches = self._match_files(photo_files, source_files)

        if not self._confirm_copy(matches):
            raise UserCancelledError

        if not self.dest_dir.exists() and not self._confirm_create_dest_dir():
            raise UserCancelledError

        self.dest_dir.mkdir(parents=True, exist_ok=True)
        self._copy_files(matches)
