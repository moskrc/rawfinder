import shutil
from pathlib import Path
from typing import Optional

from rawfinder.exceptions import OverwriteDisabledError
from rawfinder.integrity import FileIntegrityChecker


class FileCopier:
    def __init__(self, overwrite: bool = False, dry_run: bool = False, verifier: Optional[FileIntegrityChecker] = None):
        self.overwrite = overwrite
        self.dry_run = dry_run
        self.verier = verifier

    def copy(self, src: Path, dest_dir: Path) -> bool:
        dest = dest_dir / src.name

        if not self.dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            if dest.exists() and not self.overwrite:
                raise OverwriteDisabledError(str(dest))

        if not self.dry_run:
            self._perform_copy(src, dest)

        if self.verier and not self.dry_run:
            self.verier.verify_copy(src, dest)

        return True

    def _perform_copy(self, src: Path, dest: Path) -> None:
        shutil.copy2(src, dest)
