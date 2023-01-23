# RawFinder - Find a corresponded raw file

## What is it?

This script find a corresponded raw files for jpeg files in a directory.

## How to install

```bash
$ pip install rawfinder
```

## How to use
```bash
$ rawfinder -h

usage: rawfinder [-h] [-d DST] [jpeg] [raw]

Find correspond raw files

positional arguments:
  jpeg               directory with jpeg files
  raw                directory with source RAW files

options:
  -h, --help         show this help message and exit
  -d DST, --dst DST  destination dir
```

## Example

Find raw files in ~/Pictures/raw folder for jpeg files in current
folder, copy them to `raw` folder inside current folder (name by
default):

```bash
$ rawfinder . ~/Pictures/raw -dst ./raw
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
