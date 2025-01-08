import asyncio
import pathlib

import aiofiles
from loguru import logger

from rawfinder.finders import JpegFinder, RawFinder
from rawfinder.indexers import FileStorage


class App:
    DEFAULT_DST_FOLDER = pathlib.Path("raw")
    BATCH_SIZE = 10

    def __init__(
        self,
        jpeg_images_path: pathlib.Path,
        raw_images_path: pathlib.Path,
        raw_images_dest_path: pathlib.Path,
    ):
        self.jpeg_finder = JpegFinder(jpeg_images_path)
        self.raw_finder = RawFinder(raw_images_path)
        self.raw_images_dest_path = raw_images_dest_path

        self.raw_images_dest_path = (
            raw_images_dest_path if raw_images_dest_path else jpeg_images_path / self.DEFAULT_DST_FOLDER
        )
        self.sem = asyncio.Semaphore(5)

    async def get_user_confirmation(self) -> None:
        """
        Prompts the user for confirmation to proceed.
        """
        message = (
            f"JPEGs folder: '{self.jpeg_finder.path}'\n"
            f"RAWs folder: '{self.raw_finder.path}'\n"
            f"Destination folder: '{self.raw_images_dest_path}'\n"
            "This script will find corresponding RAW files for these JPEG files and copy them to the destination folder.\n"
            "Is it ok: [Y/n] "
        )

        if input(message).lower() not in ["y", ""]:
            raise KeyboardInterrupt("Cancelled.")

    async def prepare_destination(self) -> None:
        logger.info(f"Creating destination folder: {self.raw_images_dest_path}")
        self.raw_images_dest_path.mkdir(exist_ok=True, parents=True)

    async def copy_file(self, src: pathlib.Path, dst: pathlib.Path, jpeg_name: str) -> None:
        dst = dst / src.name
        async with self.sem, aiofiles.open(src, "rb") as src_file, aiofiles.open(dst, "wb") as dst_file:
            while chunk := await src_file.read(16 * 1024 * 1024):
                await dst_file.write(chunk)
            logger.info(f"RAW file {src.name} found for {jpeg_name}, has been copied to {dst}...")

    async def process_files(self) -> None:
        logger.debug("Indexing RAW files")

        storage = FileStorage()
        await storage.make_index(self.raw_finder.find())

        logger.debug("Processing JPEG files")

        tasks = []

        for jpeg_file in self.jpeg_finder.find():
            raw_file = await storage.get(jpeg_file.stem.lower())
            if raw_file:
                tasks.append(self.copy_file(raw_file, self.raw_images_dest_path, jpeg_file.name))
            else:
                logger.warning(f"No RAW file found for {jpeg_file.name}!")

        logger.debug(f"Total files to process: {len(tasks)}")

        for i in range(0, len(tasks), self.BATCH_SIZE):
            await asyncio.gather(*tasks[i : i + self.BATCH_SIZE])

    async def start(self) -> None:
        """
        Starts the application workflow.
        """
        try:
            await self.get_user_confirmation()
            await self.prepare_destination()
            await self.process_files()
            logger.info("Done.")
        except KeyboardInterrupt:
            pass
