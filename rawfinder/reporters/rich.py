from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeElapsedColumn

from rawfinder.reporters import ProgressReporter


class RichProgressReporter(ProgressReporter):
    def __init__(self) -> None:
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TextColumn("[progress.details]{task.fields[details]}"),
            transient=True,
        )

    def start(self, total: int, description: str) -> None:
        self._progress.__enter__()
        self._task_id = self._progress.add_task(description, total=total, details="Initializing...")

    def update(self, file: str, success: bool, description: str, advance: int = 1) -> None:
        self._progress.update(self._task_id, advance=advance, details=description)

    def complete(self) -> None:
        self._progress.__exit__(None, None, None)
