[![PyPI](https://img.shields.io/pypi/v/simplesam.svg?)](https://pypi.org/project/mergeBams/)
<!-- [![Build Status](https://travis-ci.org/mdshw5/simplesam.svg?branch=master)](https://travis-ci.org/mdshw5/simplesam) -->
[![Documentation Status](https://readthedocs.org/projects/mergeBams/badge/?version=latest)](https://mergeBams.readthedocs.io/en/latest/?badge=latest)

# mergeBams
==========

version 0.11

Merge sam/bam files with intelligent cell barcode preservation

## Requirements

1. Python > 3.5 (mergeBams uses the pysam package but will attempt to install if not already installed)

## Installation of pipx

```bash
module load Python
python3 -m pip install --user pipx
python3 -m pipx ensurepath

```
## Installation of mergeBams

```bash
pipx install --include-deps mergeBams
```

## Test installation of mergeBams

You should then be able to test installation by calling mergeBams.  After running the folllowing, you should see the help screen displayed.

```bash
mergeBams -h
```



## Usage

```bash
usage: mergeBams [-h] -i INPUTS [-l LABELS] [-b BCS] [-o OUT]
                 [--cell_tag CELL_TAG]

merge sam/bam files with intelligent cell barcode preservation

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTS, --inputs INPUTS
                        sam/bam input files, comma-separated
  -l LABELS, --labels LABELS
                        strings for prepending cell barcode (i.e. sample
                        name), comma-separated
  -b BCS, --bcs BCS     barcodes files, comma-separated
  -o OUT, --out OUT     outdir
  --cell_tag CELL_TAG   set if cell barcode tag should not be CB
```


## Acknowledgements

Written by Scott Furlan