# RawFinder - Find a corresponded raw file

**RawFinder** is a Python tool to help photographers and image processors locate and manage RAW files corresponding to JPEG images. It efficiently scans directories, searches for matching RAW files, and moves them to a specified location.

## Installation

Install via pip:

```bash
$ pip install rawfinder
```

## How to use

```bash
$ rawfinder -h

Usage: rawfinder [OPTIONS] IMAGES_DIR SOURCES_DIR [DEST_SOURCES_DIR]

  Find corresponding RAW files for JPEG images and copy them to a DEST folder.

  JPEG_DIR - directory with JPEG files.
  RAW_DIR  - directory with RAW files.
  DEST_DIR - destination directory for RAW files.
             default is 'raw' inside the JPEG_DIR

Options:
  --help  Show this message and exit.
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
