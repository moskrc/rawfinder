import logging
import sys
from pathlib import Path
from typing import Optional

try:
    from rich.logging import RichHandler as _RichHandler

    rich_handler: Optional[type[_RichHandler]] = _RichHandler
except ImportError:
    rich_handler = None


def setup_logging(verbose: bool = False, handler_type: Optional[str] = None, log_file: Optional[Path] = None) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%H:%M:%S"

    # Explicitly declare the list as containing logging.Handler objects.
    handlers: list[logging.Handler] = []
    console_handler: logging.Handler = logging.StreamHandler(sys.stdout)

    if handler_type == "rich":
        if rich_handler is None:
            logging.warning("Rich is not installed, using default handler")
            console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
        else:
            console_handler = rich_handler(rich_tracebacks=True)
            console_handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    handlers.append(console_handler)

    if log_file:
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler: logging.Handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
            handlers.append(file_handler)
        except Exception as e:
            logging.warning(f"Failed to set up file logging to {log_file}: {e!s}")

    logging.basicConfig(level=level, handlers=handlers, force=True)
