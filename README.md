[![PyPI](https://img.shields.io/pypi/v/simplesam.svg?)](https://pypi.org/project/mergeBams/)
<!-- [![Build Status](https://travis-ci.org/mdshw5/simplesam.svg?branch=master)](https://travis-ci.org/mdshw5/simplesam) -->

# mergeBams
==========

version 0.14

Merge sam/bam files with intelligent cell barcode preservation.  This has been tested on bam file and tsv output from the 10X Genomics Cellranger program.  The implementation of mergeBams was motivated by and primarily designed for working with Cellranger output.

## Requirements

1. Python > 3.5 (mergeBams uses the pysam package but will attempt to install if not already installed)

## Installation of pipx

```bash
module load Python
python3 -m pip install --user pipx
python3 -m pipx ensurepath

```

To read more about pipx, please visit https://github.com/pipxproject/pipx.



## Installation of mergeBams

With pipx installed, installation of mergeBams is trivial.

```bash
pipx install --include-deps mergeBams
```

## Test installation of mergeBams

You should then be able to test installation by calling mergeBams.  After running the folllowing, you should see the help screen displayed.

```bash
mergeBams -h
```

## Help

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

## Usage

The following is an example of merging two bam files and two barcodes.tsv files that were derived from them.

```bash
mergeBams -i t1.bam,t2.bam \
          -l t1_,t2_ \
          -b barcodes1.tsv,barcodes2.tsv \
          -o /home/user/test
```

## Expected output

**In the above example mergeBams will take input bams t1.bam and t2.bam which have the following data...**

```bash
samtools view t1.bam | head -n 3 -
```

```bash
A00613:162:HKWCTDRXX:1:1228:5330:21151  272 1 12048 0 91M * 0 0 GCAAGCTGAGCACTGGAGTGGAGTTTTCCTGTGGAGAGGAGCCATGCCTAGAGTGGGATGGGCCATTGTTCATCTTCTGGCCCCTGTTGTC FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF NH:i:7  HI:i:4  AS:i:89 nM:i:0  RE:A:I  li:i:0  BC:Z:GCTGTCCA QT:Z:FFFFFFFF CR:Z:ACACCAAAGGTTCCTA CY:Z:FFFFFFFFFFFFFFFF CB:Z:ACACCAAAGGTTCCTA-1 UR:Z:ACCAGTCGGT UY:Z:FFFFFFFFFF UB:Z:ACCAGTCGGT RG:Z:B1_GEX:0:1:HKWCTDRXX:1
A00613:162:HKWCTDRXX:1:1166:7455:25708  256 1 16724 0 42M92N49M * 0 0 GTGGGGGCGGTGGTGGTGCTGTTAGTACCCCATCTTGTAGGTCTTGAGAGGCTCGGCTACCTCAGTGTGGAAGGTGGGCAGTTCTGGAATG FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF NH:i:6  HI:i:4  AS:i:85 nM:i:2  RE:A:I  li:i:0  BC:Z:TTGAGATC QT:Z:FFFFFFFF CR:Z:TTTATGCGTCGCCATG CY:Z:FFFFFFFFFFFFFFFFCB:Z:TTTATGCGTCGCCATG-1  UR:Z:CTAGTTGCGC UY:Z:FFFFFFFFFF UB:Z:CTAGTTGCGC RG:Z:B1_GEX:0:1:HKWCTDRXX:1
A00613:162:HKWCTDRXX:1:1272:21866:31062 256 1 18298 0 73M18S  * 0 0 CTCAATCTTGGCCTGGGCCAAGGAGACCTTCTCTCCAATGGCCTGCACCTGGCTCCGGCTCTGCTCTACCTGCGAAGTTGCTCGGCGCCCT FFFFFFFFFFFFF:FFFFFFFFFFFFFFFFFFFFFFF:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF NH:i:8  HI:i:5  AS:i:71 nM:i:0  RE:A:I  li:i:0  BC:Z:TTGAGATC QT:Z::FFFFFFF CR:Z:AACTGGTAGAGTGACC CY:Z:FFFFFFFFF:FFFFFF CB:Z:AACTGGTAGAGTGACC-1 UR:Z:GTTCACCATA UY:Z:FFFFFFFFFF UB:Z:GTTCACCATA RG:Z:B1_GEX:0:1:HKWCTDRXX:1
```

**AND**

```bash
samtools view t2.bam | tail -n 3 -
```

```bash
A00613:162:HKWCTDRXX:2:2107:15519:35790 4 * 0 0 * * 0 0 ATGAGAAGGCACCCAAGCTTTACCAATAACACCATAAGGATAGGTGCGTACACCACACGCCTCAAACGGCCCCAGATAACTGGTGTCGTCC F:F:,,:,:,,FF,F,:F:F:,FF,,FFF,,,,,,,,:F::,,:,,,F,:,FFF,,,F,:,:::,:F,,FF,,,FFF,FF,,FFF,,F,:: NH:i:0  HI:i:0  AS:i:18 nM:i:1  uT:A:1  xf:i:0  li:i:0  BC:Z:TGGAAGGT QT:Z:FF,,F,:F CR:Z:TTTGTCATCCGTTGTC CY:Z:F,FFF:,FF:F:FFFFCB:Z:TTTGTCATCCGTTGTC-1  UR:Z:TCCCGCTCAT UY:Z:FFFFFFFFFF UB:Z:TCCCGCTCAT RG:Z:B2_GEX:0:1:HKWCTDRXX:2
A00613:162:HKWCTDRXX:2:2177:9046:12085  4 * 0 0 * * 0 0 AAGCAGTGGTATCAACGCAGAGTACTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTATATT FFFFF:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:FFFFFFFFFFFFFFF:F:F:FFFFFFFFFFFFFFFFFFFF:,F,:, NH:i:0  HI:i:0  AS:i:46 nM:i:0  uT:A:1  xf:i:0  li:i:0  BC:Z:GCATCTCC QT:Z:FFFFFFFF CR:Z:TTTGTCATCCTGCAGG CY:Z:F:FFFFFFFF:FF:FFCB:Z:TTTGTCATCCTGCAGG-1  UR:Z:CTGCCTATCA UY:Z:FFFFFFFFFF UB:Z:CTGCCTATCA RG:Z:B2_GEX:0:1:HKWCTDRXX:2
A00613:162:HKWCTDRXX:2:2234:20546:22514 4 * 0 0 * * 0 0 AAGCAGTGGTATCAACGCAGAGTACTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTAGTAAAAAACACCCCCGGTGGGGGGTGGGTAATT FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:FFFFFFFFFFFFFFFFFFFFFF,,:,F:,F,,:,,FF,::,,,FF,,,,::,,,,F NH:i:0  HI:i:0  AS:i:36 nM:i:0  uT:A:1  xf:i:0  li:i:0  BC:Z:AACGTCAA QT:Z:FFFFFFFF CR:Z:TTTGTCATCGGTTCGG CY:Z:FFFFFFFFFFFFFFFFCB:Z:TTTGTCATCGGTTCGG-1  UR:Z:GCACTGCGAG UY:Z:FF:FFFFF:F UB:Z:GCACTGCGAG RG:Z:B2_GEX:0:1:HKWCTDRXX:2
```

**These bam files will be concatenated but will prepend the cell barcode (CB tag) with the label supplied in the program call using the -l flag**

```bash
(samtools view out.bam | head -n 3 -; samtools view out.bam | tail -n 3 -) > topandbottom.txt
cat topandbottom.txt
```

```bash
A00613:162:HKWCTDRXX:1:1228:5330:21151  272 1 12048 0 91M * 0 0 GCAAGCTGAGCACTGGAGTGGAGTTTTCCTGTGGAGAGGAGCCATGCCTAGAGTGGGATGGGCCATTGTTCATCTTCTGGCCCCTGTTGTC FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF NH:i:7  HI:i:4  AS:i:89 nM:i:0  RE:A:I  li:i:0  BC:Z:GCTGTCCA QT:Z:FFFFFFFF CR:Z:ACACCAAAGGTTCCTA CY:Z:FFFFFFFFFFFFFFFF UR:Z:ACCAGTCGGT UY:Z:FFFFFFFFFF UB:Z:ACCAGTCGGT RG:Z:B1_GEX:0:1:HKWCTDRXX:1 CB:Z:t1_ACACCAAAGGTTCCTA-1
A00613:162:HKWCTDRXX:1:1166:7455:25708  256 1 16724 0 42M92N49M * 0 0 GTGGGGGCGGTGGTGGTGCTGTTAGTACCCCATCTTGTAGGTCTTGAGAGGCTCGGCTACCTCAGTGTGGAAGGTGGGCAGTTCTGGAATG FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF NH:i:6  HI:i:4  AS:i:85 nM:i:2  RE:A:I  li:i:0  BC:Z:TTGAGATC QT:Z:FFFFFFFF CR:Z:TTTATGCGTCGCCATG CY:Z:FFFFFFFFFFFFFFFFUR:Z:CTAGTTGCGC  UY:Z:FFFFFFFFFF UB:Z:CTAGTTGCGC RG:Z:B1_GEX:0:1:HKWCTDRXX:1 CB:Z:t1_TTTATGCGTCGCCATG-1
A00613:162:HKWCTDRXX:1:1272:21866:31062 256 1 18298 0 73M18S  * 0 0 CTCAATCTTGGCCTGGGCCAAGGAGACCTTCTCTCCAATGGCCTGCACCTGGCTCCGGCTCTGCTCTACCTGCGAAGTTGCTCGGCGCCCT FFFFFFFFFFFFF:FFFFFFFFFFFFFFFFFFFFFFF:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF NH:i:8  HI:i:5  AS:i:71 nM:i:0  RE:A:I  li:i:0  BC:Z:TTGAGATC QT:Z::FFFFFFF CR:Z:AACTGGTAGAGTGACC CY:Z:FFFFFFFFF:FFFFFF UR:Z:GTTCACCATA UY:Z:FFFFFFFFFF UB:Z:GTTCACCATA RG:Z:B1_GEX:0:1:HKWCTDRXX:1 CB:Z:t1_AACTGGTAGAGTGACC-1
A00613:162:HKWCTDRXX:2:2107:15519:35790 4 * 0 0 * * 0 0 ATGAGAAGGCACCCAAGCTTTACCAATAACACCATAAGGATAGGTGCGTACACCACACGCCTCAAACGGCCCCAGATAACTGGTGTCGTCC F:F:,,:,:,,FF,F,:F:F:,FF,,FFF,,,,,,,,:F::,,:,,,F,:,FFF,,,F,:,:::,:F,,FF,,,FFF,FF,,FFF,,F,:: NH:i:0  HI:i:0  AS:i:18 nM:i:1  uT:A:1  xf:i:0  li:i:0  BC:Z:TGGAAGGT QT:Z:FF,,F,:F CR:Z:TTTGTCATCCGTTGTC CY:Z:F,FFF:,FF:F:FFFFUR:Z:TCCCGCTCAT  UY:Z:FFFFFFFFFF UB:Z:TCCCGCTCAT RG:Z:B2_GEX:0:1:HKWCTDRXX:2 CB:Z:t2_TTTGTCATCCGTTGTC-1
A00613:162:HKWCTDRXX:2:2177:9046:12085  4 * 0 0 * * 0 0 AAGCAGTGGTATCAACGCAGAGTACTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTATATT FFFFF:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:FFFFFFFFFFFFFFF:F:F:FFFFFFFFFFFFFFFFFFFF:,F,:, NH:i:0  HI:i:0  AS:i:46 nM:i:0  uT:A:1  xf:i:0  li:i:0  BC:Z:GCATCTCC QT:Z:FFFFFFFF CR:Z:TTTGTCATCCTGCAGG CY:Z:F:FFFFFFFF:FF:FFUR:Z:CTGCCTATCA  UY:Z:FFFFFFFFFF UB:Z:CTGCCTATCA RG:Z:B2_GEX:0:1:HKWCTDRXX:2 CB:Z:t2_TTTGTCATCCTGCAGG-1
A00613:162:HKWCTDRXX:2:2234:20546:22514 4 * 0 0 * * 0 0 AAGCAGTGGTATCAACGCAGAGTACTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTAGTAAAAAACACCCCCGGTGGGGGGTGGGTAATT FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:FFFFFFFFFFFFFFFFFFFFFF,,:,F:,F,,:,,FF,::,,,FF,,,,::,,,,F NH:i:0  HI:i:0  AS:i:36 nM:i:0  uT:A:1  xf:i:0  li:i:0  BC:Z:AACGTCAA QT:Z:FFFFFFFF CR:Z:TTTGTCATCGGTTCGG CY:Z:FFFFFFFFFFFFFFFFUR:Z:GCACTGCGAG  UY:Z:FF:FFFFF:F UB:Z:GCACTGCGAG RG:Z:B2_GEX:0:1:HKWCTDRXX:2 CB:Z:t2_TTTGTCATCGGTTCGG-1
```

Similarly and if desired, mergeBams will concatenate and add labels to barcodes.tsv files (for compressed barcodes.tsv.gz see below for an explanation of how compression of barcodes files are handled).  For example, in the above case...


```bash
head -n 3 barcodes1.tsv
```

```bash
AAACCTGAGCCCGAAA-1
AAACCTGAGGTGCTTT-1
AAACCTGAGTACTTGC-1
```

**AND**

```bash
tail -n 3 barcodes2.tsv
```

```bash
TTTGTCATCATTCACT-1
TTTGTCATCCGTTGTC-1
TTTGTCATCCTGCAGG-1
```

Will be joined and given labels.

```bash
(head -n 3 outbcs.tsv; tail -n 3 outbcs.tsv) > topandbottombc.txt
cat topandbottombc.txt
```

```bash
t1_AAACCTGAGCCCGAAA-1
t1_AAACCTGAGGTGCTTT-1
t1_AAACCTGAGTACTTGC-1
t2_TTTGTCATCATTCACT-1
t2_TTTGTCATCCGTTGTC-1
t2_TTTGTCATCCTGCAGG-1
```


Note that this program is compression aware and will compress output of barcodes file to match input. I.e. the following will produce compressed barcode file as output.  All supplied barcodes files must either be all compressed or all uncompressed.

```bash
mergeBams -i t1.bam,t2.bam \
          -l t1_,t2_ \
          -b barcodes1.tsv.gz,barcodes2.tsv.gz \
          -o /home/user/test
```


## Acknowledgements

Written by Scott Furlan with help from cfcooldood and rcguy