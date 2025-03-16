import logging
import time
from typing import Optional

from rawfinder.reporters import ProgressReporter


class PlainProgressReporter(ProgressReporter):
    def __init__(self) -> None:
        self.start_time: Optional[float] = None
        self.total = 0
        self.current = 0
        self.logger = logging.getLogger(__name__)

    def start(self, total: int, description: str) -> None:
        self.total = total
        self.current = 0
        self.start_time = time.time()
        self.logger.info(f"{description} [0/{self.total}]")

    def update(self, file: str, success: bool, description: str, advance: int = 1) -> None:
        self.current += advance
        if self.start_time is None:
            raise RuntimeError
        elapsed = time.time() - self.start_time
        self.logger.info(f"[{self.current}/{self.total}] {file} - {description} (Elapsed: {elapsed:.1f}s)")

    def complete(self) -> None:
        if self.start_time is None:
            raise RuntimeError
        elapsed = time.time() - self.start_time
        self.logger.info(f"Completed {self.current}/{self.total} files in {elapsed:.1f} seconds")
