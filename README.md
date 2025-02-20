# RawFinder - Find a corresponded raw file

**RawFinder** is a Python tool to help photographers and image processors locate and manage RAW files corresponding to JPEG images. It efficiently scans directories, searches for matching RAW files, and moves them to a specified location.

## Installation

Install via pipx:

```bash
$ pipx install rawfinder
```

## How to use

```bash
$ rawfinder -h

usage: rawfinder [-h] jpeg_dir raw_dir dest_dir

Find RAW files for JPEG files and copy them to the destination directory.

positional arguments:
  jpeg_dir    Directory with JPEG files.
  raw_dir     Directory with RAW files.
  dest_dir    Destination directory for copied RAW files.

options:
  -h, --help  show this help message and exit
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
