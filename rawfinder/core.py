import argparse
import os
import pathlib
import shutil
from typing import Optional
from rawfinder.finders import JpegFinder, RawFinder
from rawfinder.indexers import FileStorage
from loguru import logger

DEFAULT_DST_FOLDER = pathlib.Path("raw")


class UserInteraction:
    @staticmethod
    def confirm_action(message: str) -> bool:
        return input(message).lower() in ["y", ""]


class FileCopier:
    def __init__(
        self,
        jpeg_finder: JpegFinder,
        raw_finder: RawFinder,
        dest_path: pathlib.Path,
        storage: FileStorage,
        copier=shutil.copy,
    ):
        self.jpeg_finder = jpeg_finder
        self.raw_finder = raw_finder
        self.dest_path = dest_path
        self.storage = storage
        self.copier = copier

    def prepare_destination(self):
        logger.info(f"Creating destination folder: {self.dest_path}")
        self.dest_path.mkdir(exist_ok=True, parents=True)

    def process_files(self):
        logger.debug("Indexing RAW files")
        self.storage.make_index(self.raw_finder.find())

        logger.debug("Processing JPEG files")
        for jpeg_file in self.jpeg_finder.find():
            raw_file = self.storage.get(jpeg_file.stem.lower())
            if raw_file:
                logger.info(
                    f"RAW file {raw_file.name} found for {jpeg_file.name}, copying to {self.dest_path}..."
                )
                self.copier(raw_file, self.dest_path)
            else:
                logger.warning(f"No RAW file found for {jpeg_file.name}!")


class App:
    def __init__(
        self,
        jpeg_images_path: str,
        raw_images_path: str,
        raw_images_dest_path: Optional[str] = None,
    ):
        self.jpeg_finder = JpegFinder(jpeg_images_path)
        self.raw_finder = RawFinder(raw_images_path)
        self.dest_path = (
            pathlib.Path(raw_images_dest_path)
            if raw_images_dest_path
            else pathlib.Path(jpeg_images_path) / DEFAULT_DST_FOLDER
        )
        self.storage = FileStorage()
        self.copier = FileCopier(
            self.jpeg_finder, self.raw_finder, self.dest_path, self.storage
        )

    def get_user_confirmation(self) -> None:
        """
        Prompts the user for confirmation to proceed.
        """
        message = (
            f"JPEGs folder: '{self.jpeg_finder.path}'\n"
            f"RAWs folder: '{self.raw_finder.path}'\n"
            f"Destination folder: '{self.dest_path}'\n"
            "This script will find corresponding RAW files for these JPEG files and copy them to the destination folder.\n"
            "Is it ok: [Y/n] "
        )
        if not UserInteraction.confirm_action(message):
            raise KeyboardInterrupt("Operation cancelled by the user.")

    def start(self) -> None:
        """
        Starts the application workflow.
        """
        try:
            self.get_user_confirmation()
            self.copier.prepare_destination()
            self.copier.process_files()
            logger.info("Done.")
        except KeyboardInterrupt:
            pass


def main():
    parser = argparse.ArgumentParser(
        prog="rawfinder", description="Find corresponding raw files for images"
    )
    parser.add_argument(
        "image_dir", nargs="?", help="Directory with images", default=os.getcwd()
    )
    parser.add_argument("raw_dir", nargs="?", help="Directory with RAW files")
    parser.add_argument("-t", "--target", help="Destination directory", required=False)
    args = parser.parse_args()

    app = App(args.image_dir, args.raw_dir, args.target)
    app.start()


if __name__ == "__main__":
    main()
