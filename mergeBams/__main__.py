import sys
import argparse
import os
from . import mergeBams

def run_BamMerge(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description = 'merge sam/bam files with intelligent cell barcode preservation')
    parser.add_argument('-i', '--inputs', required = True, help = "sam/bam input files, comma-separated")
    parser.add_argument('-l', '--labels', required = False, help = "strings for prepending cell barcode (i.e. sample name), comma-separated")
    parser.add_argument('-b', '--bcs', required = False, help = "barcodes files, comma-separated")
    parser.add_argument('-o', '--out', required = False, help = "outdir")
    parser.add_argument("--cell_tag", required = False, default = "CB", help = "set if cell barcode tag should not be CB")
    args = parser.parse_args()

    BamMerge = mergeBams.BamMerge(cli_args = args)
    BamMerge.merge()


if __name__ == "__main__":
    run_BamMerge()

# debugging call
"""
call = 'merge_bams.py -i t1.bam,t2.bam -l t1_,t2_'
args = parser.parse_args(call.split(" ")[1:])
"""