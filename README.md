# RawFinder - Find a corresponded raw file

## What is it?

This script finds corresponded RAW files for images.

## How to install

```bash
$ pip install rawfinder
```

## How to use
```bash
$ rawfinder -h

usage: rawfinder [-h] [-t TARGET] [image_dir] [raw_dir]

Find corresponding raw files for images

positional arguments:
  image_dir             directory with images
  raw_dir               directory with RAW files

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        destination dir
```

## Example

Find raw files in ~/Pictures/raw folder for jpeg files in current
folder, copy them to `raw` folder inside current folder (name by
default):

```bash
$ rawfinder . ~/Pictures/raw -t ./raw
```

# Development

## Install

```bash
$ poetry install
```

## Tests

```bash
$ poetry run make test
```

## Linters

```bash
$ poetry run make format
```
