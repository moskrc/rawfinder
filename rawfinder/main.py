import argparse
import asyncio
import logging
from pathlib import Path

from rawfinder.app import AsyncRawFinderApp


def setup_logger() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find RAW files for JPEG files and copy them to the destination directory."
    )
    parser.add_argument("jpeg_dir", type=Path, help="Directory with JPEG files.")
    parser.add_argument("raw_dir", type=Path, help="Directory with RAW files.")
    parser.add_argument("dest_dir", type=Path, help="Destination directory for copied RAW files.")
    return parser.parse_args()


async def main_async() -> None:
    args = parse_args()
    logger = setup_logger()
    app = AsyncRawFinderApp(args.jpeg_dir, args.raw_dir, args.dest_dir, logger)
    await app.run()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
