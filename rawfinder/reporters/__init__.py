from typing import Protocol


class ProgressReporter(Protocol):
    def start(self, total: int, description: str) -> None: ...

    def update(self, file: str, success: bool, description: str, advance: int = 1) -> None: ...

    def complete(self) -> None: ...
