import logging
import sys
from pathlib import Path

try:
    from rich.logging import RichHandler
except ImportError:
    RichHandler = None


def setup_logging(verbose: bool = False, handler_type: str | None = None, log_file: Path | None = None) -> None:
    level = logging.DEBUG if verbose else logging.INFO

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%H:%M:%S"

    handlers = []

    try:
        from rich.logging import RichHandler
    except ImportError:
        RichHandler = None

    if handler_type == "rich":
        if RichHandler is None:
            logging.warning("Rich is not installed, falling back to default handler")
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
        else:
            console_handler = RichHandler(rich_tracebacks=True)
            console_handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    handlers.append(console_handler)

    if log_file:
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
            handlers.append(file_handler)
        except Exception as e:
            logging.warning(f"Failed to set up file logging to {log_file}: {e!s}")

    logging.basicConfig(level=level, handlers=handlers, force=True)
