from email.policy import default
from pathlib import Path

import click

from rawfinder.app import App


@click.command()
@click.argument("images_dir", type=click.Path(exists=True))
@click.argument("sources_dir", type=click.Path(exists=True))
@click.argument("dest_sources_dir", default="", type=click.Path(writable=True))
def main(images_dir, sources_dir, dest_sources_dir):
    """Find corresponding RAW files for JPEG images and copy them to a DEST folder.

    \b
    JPEG_DIR - directory with JPEG files.
    RAW_DIR  - directory with RAW files.
    DEST_DIR - destination directory for RAW files.
               default is 'raw' inside the JPEG_DIR
    """

    app = App(
        images_dir,
        sources_dir,
        dest_sources_dir,
    )
    app.start()


if __name__ == "__main__":
    main()
