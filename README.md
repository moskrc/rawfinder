# RawFinder - Find a corresponded raw file

**RawFinder** is a Python tool to help photographers and image processors locate and manage RAW files corresponding to JPEG images. It efficiently scans directories, searches for matching RAW files, and moves them to a specified location.

## Installation

Install via pipx:

```bash
$ pipx install rawfinder
```

## How to use

```bash
$ rawfinder

Usage: rawfinder [OPTIONS] COMMAND [ARGS]...

  RAW Photo Organizer CLI Tool

Options:
  --verbose              Enable debug output
  --config PATH          Custom config file path
  --handler-type [rich]  Type of logging handler (rich for colorful output,
                         default for standard)
  --log-file PATH        Path to file where logs will be written
  --help                 Show this message and exit.

Commands:
  process  Organize RAW photos by matching them with JPEG counterparts.
  config   Manage application configuration

   poetry run rawfinder config                                                                                                             [.venv] vit@Vitaliis-MacBook-Air
```

```bash
$ rawfinder config
Usage: rawfinder config [OPTIONS] COMMAND [ARGS]...

  Manage application configuration

Options:
  --help  Show this message and exit.

Commands:
  init      Initialize configuration file
  path      Show config file location
  edit      Edit config file in default editor
  delete    Delete config file
  validate  Validate current configuration
```

```bash
$ rawfinder process
Usage: rawfinder process [OPTIONS] PHOTOS_DIR SOURCES_DIR DEST_DIR

  Organize RAW photos by matching them with JPEG counterparts.

  PHOTOS_DIR - directory with photos (JPEG files)

  SOURCES_DIR - directory with sources files (RAW files)

  DEST_DIR - destination directory for sources (RAW files matched with JPEGs)

  Note: Global options like --verbose, --config, --handler-type, and --log-
  file can also be used.

  Use `--log-file PATH` to write logs to a file. Run `rawfinder --help` for
  details on global options.

Options:
  --overwrite
  --dry-run                       Simulate operations without actual changes
  --reporter [rich|plain]         Progress reporting style
  --verify-checksum STR_TO_BOOL   Verify checksums of copied files
  --verify-checksum-chunk-size INTEGER
                                  Chunk size for verifying checksums
  --photos-extensions TEXT        Custom photos file extensions (e.g.,
                                  --photos-extensions .bmp --photos-extensions
                                  .png)
  --sources-extensions TEXT       Custom source file extensions (e.g.,
                                  --sources-extensions .tiff --sources-
                                  extensions .pdf)
  --help                          Show this message and exit.
```

## Example

Find raw files in ~/Pictures/raw folder for jpeg files in current
folder, copy them to `raw` folder inside current folder (name by
default):

```bash
$ rawfinder . ~/Pictures/raw ./raw
```

# Development

## Install

```bash
$ make install
```

## Tests

```bash
$ make test
```

## Linters

```bash
$ make check
```
