import logging
from pathlib import Path

import click
import yaml

from rawfinder.app import RawFinderApp
from rawfinder.config import AppConfig, ConfigLoader, ConfigManager, ReporterEnum
from rawfinder.copier import FileCopier
from rawfinder.exceptions import (
    BooleanValueExpectedError,
    UnknownReporterError,
    UserCancelledError,
    WriteConfigFileError,
)
from rawfinder.integrity import FileIntegrityChecker
from rawfinder.logging import setup_logging
from rawfinder.reporters import ProgressReporter
from rawfinder.reporters.factories import ReporterFactory

logger = logging.getLogger(__name__)


def str_to_bool(value: str) -> bool:
    if isinstance(value, bool):
        return value
    value = value.lower()
    if value in ("true", "t", "yes", "y", "1"):
        return True
    elif value in ("false", "f", "no", "n", "0"):
        return False
    else:
        raise BooleanValueExpectedError(value)


class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx: click.Context) -> list[str]:
        return list(self.commands.keys())


@click.group(cls=NaturalOrderGroup)
@click.option("--verbose", is_flag=True, help="Enable debug output")
@click.option("--config", type=click.Path(path_type=Path), help="Custom config file path")
@click.option(
    "--handler-type",
    type=click.Choice(["rich"], case_sensitive=False),
    default=None,
    help="Type of logging handler (rich for colorful output, default for standard)",
)
@click.option(
    "--log-file", type=click.Path(path_type=Path), default=None, help="Path to file where logs will be written"
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, config: Path, handler_type: str, log_file: Path) -> None:
    """RAW Photo Organizer CLI Tool"""
    setup_logging(verbose=verbose, handler_type=handler_type, log_file=log_file)
    ctx.ensure_object(dict)

    cfg_loader = ConfigLoader(config_path=config)
    ctx.obj["config"] = cfg_loader.load()


@cli.command()
@click.argument(
    "photos_dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        path_type=Path,
    ),
)
@click.argument("sources_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("dest_dir", type=click.Path(path_type=Path))
@click.option("--overwrite", is_flag=True, default=None)
@click.option("--dry-run", is_flag=True, default=None, help="Simulate operations without actual changes")
@click.option(
    "--reporter-type",
    default=None,
    type=click.Choice([item.value for item in ReporterEnum]),
    help="Progress reporting style",
)
@click.option(
    "--verify-checksum",
    type=str_to_bool,
    default=None,
    help="Verify checksums of copied files",
)
@click.option(
    "--verify-checksum-chunk-size",
    type=int,
    default=None,
    help="Chunk size for verifying checksums",
    show_default=True,
)
@click.option(
    "--photos-extensions",
    type=str,
    multiple=True,
    default=None,
    help="Custom photos file extensions (e.g., --photos-extensions .bmp --photos-extensions .png)",
)
@click.option(
    "--sources-extensions",
    type=str,
    default=None,
    multiple=True,
    help="Custom source file extensions (e.g., --sources-extensions .tiff --sources-extensions .pdf)",
)
@click.pass_context
def process(
    ctx: click.Context,
    photos_dir: Path,
    sources_dir: Path,
    dest_dir: Path,
    verify_checksum: bool,
    verify_checksum_chunk_size: int,
    overwrite: bool,
    dry_run: bool,
    reporter_type: str,
    photos_extensions: tuple[str, ...],
    sources_extensions: tuple[str, ...],
) -> None:
    """Organize RAW photos by matching them with JPEG counterparts.

    PHOTOS_DIR - directory with photos (JPEG files)

    SOURCES_DIR - directory with sources files (RAW files)

    DEST_DIR - destination directory for sources (RAW files matched with JPEGs)

    Note: Global options like --verbose, --config, --handler-type, and --log-file can also be used.

    Use `--log-file PATH` to write logs to a file. Run `rawfinder --help` for details on global options.
    """
    config: AppConfig = ctx.obj["config"]

    config.overwrite = overwrite or config.overwrite
    config.dry_run = dry_run or config.dry_run
    config.reporter = ReporterEnum(reporter_type) if reporter_type else config.reporter
    config.verify_checksum = verify_checksum if verify_checksum is not None else config.verify_checksum
    config.verify_checksum_chunk_size = verify_checksum_chunk_size or config.verify_checksum_chunk_size

    if photos_extensions:
        config.extensions["photos"] = list(photos_extensions)
    if sources_extensions:
        config.extensions["sources"] = list(sources_extensions)

    logger.debug("Configuration:")
    logger.debug(yaml.safe_dump(config.model_dump(mode="json"), sort_keys=False))

    try:
        check_sum_verifier = (
            FileIntegrityChecker(chunk_size=config.verify_checksum_chunk_size) if config.verify_checksum else None
        )

        copier = FileCopier(overwrite=config.overwrite, dry_run=config.dry_run, verifier=check_sum_verifier)

        reporter: ProgressReporter = ReporterFactory.create(config.reporter.value)

        app = RawFinderApp(
            photos_dir=photos_dir,
            sources_dir=sources_dir,
            dest_dir=dest_dir,
            copier=copier,
            progress_reporter=reporter,
            dry_run=config.dry_run,
            photo_extensions=config.extensions["photos"],
            source_extensions=config.extensions["sources"],
        )

        app.run()
    except UnknownReporterError as e:
        logger.warning("Invalid reporter type: {}", e.reporter_type)
        raise click.Abort() from e
    except UserCancelledError:
        pass
    except Exception as e:
        logger.exception("Unexpected error")
        raise click.Abort() from e
    else:
        logger.info("Processing completed successfully!")


@cli.group(cls=NaturalOrderGroup)
def config() -> None:
    """Manage application configuration"""
    pass


@config.command()
@click.option("--force", is_flag=True, help="Overwrite existing config")
@click.pass_context
def init(ctx: click.Context, force: bool) -> None:
    """Initialize configuration file"""
    cfg_path = ConfigManager.get_user_config_path()

    if cfg_path.exists() and not force:
        logger.info(f"Config already exists at {cfg_path}")
        return

    try:
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        with cfg_path.open("w") as f:
            yaml.safe_dump(AppConfig().model_dump(mode="json"), f, sort_keys=False)
    except Exception as e:
        cfg_path.unlink()
        cfg_path.parent.rmdir()
        raise WriteConfigFileError from e

    logger.info(f"Config created at {cfg_path}")


@config.command()
@click.pass_context
def path(ctx: click.Context) -> None:
    """Show config file location"""
    cfg_path = ConfigManager.get_user_config_path()
    logger.info(f"User config: {cfg_path}")
    if not cfg_path.exists():
        logger.warning("Config file does not exist")


@config.command()
@click.pass_context
def edit(ctx: click.Context) -> None:
    """Edit config file in default editor"""
    cfg_path = ConfigManager.get_user_config_path()
    if not cfg_path.exists():
        ctx.invoke(init)

    # Открываем файл в редакторе, используя click.edit()
    updated_content = click.edit(filename=str(cfg_path))
    if updated_content is not None:
        # Если пользователь что-то изменил, перезаписываем файл
        with open(cfg_path, "w") as f:
            f.write(updated_content)
        logger.info("Config updated")
    else:
        logger.info("No changes made to the config")


@config.command()
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete config file"""
    cfg_path = ConfigManager.get_user_config_path()
    if cfg_path.exists():
        cfg_path.unlink()
        logger.info("Config deleted")
    else:
        logger.info("Config file does not exist")


@config.command()
@click.pass_context
def validate(ctx: click.Context) -> None:
    """Validate current configuration"""
    try:
        cfg = ConfigLoader().load()
        logger.info("Configuration is valid")
        logger.info(yaml.safe_dump(cfg.model_dump(mode="json"), sort_keys=False))
    except Exception as e:
        logger.info(f"Invalid config: {e!s}")
        raise click.Abort() from e
