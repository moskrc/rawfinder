import pathlib
import shutil
from rawfinder.finders import JpegFinder, RawFinder
from rawfinder.indexers import FileStorage
from loguru import logger


class App:
    DEFAULT_DST_FOLDER = pathlib.Path("raw")

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
            raw_images_dest_path
            if raw_images_dest_path
            else jpeg_images_path / self.DEFAULT_DST_FOLDER
        )

    def get_user_confirmation(self) -> None:
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

        if not input(message).lower() in ["y", ""]:
            raise KeyboardInterrupt("Operation cancelled by the user.")

    def prepare_destination(self):
        logger.info(f"Creating destination folder: {self.raw_images_dest_path}")
        self.raw_images_dest_path.mkdir(exist_ok=True, parents=True)

    def process_files(self):
        logger.debug("Indexing RAW files")

        storage = FileStorage()
        storage.make_index(self.raw_finder.find())

        logger.debug("Processing JPEG files")

        for jpeg_file in self.jpeg_finder.find():
            raw_file = storage.get(jpeg_file.stem.lower())
            if raw_file:
                logger.info(
                    f"RAW file {raw_file.name} found for {jpeg_file.name}, copying to {self.raw_images_dest_path}..."
                )
                shutil.copy(raw_file, self.raw_images_dest_path)
            else:
                logger.warning(f"No RAW file found for {jpeg_file.name}!")

    def start(self) -> None:
        """
        Starts the application workflow.
        """
        try:
            self.get_user_confirmation()
            self.prepare_destination()
            self.process_files()
            logger.info("Done.")
        except KeyboardInterrupt:
            pass
