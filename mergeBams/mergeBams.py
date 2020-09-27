#!/usr/bin/env python
import os
import sys
import pysam
import csv
import binascii
import gzip
import shutil

magic_dict = {
    b"\x8b\x1f": "gz",
    b"\x1f\x8b\x08": "gz",
    b"\x42\x5a\x68": "bz2",
    b"\x50\x4b\x03\x04": "zip"
    }

max_len = max(len(x) for x in magic_dict)

def file_type(filename):
    with open(filename, "rb") as f:
        file_start = f.read(max_len)
    for magic, filetype in magic_dict.items():
        if file_start.startswith(magic):
            return filetype
    return "no match"


def checkEqual(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)

# def is_gz_file(filepath):
#     f = open(filepath)
#     print(f.read(2))
#     isg = f.read(2)=="1f8b"
#     f.close()
#     return(isg)
    # with open(filepath, 'rb') as test_f:
    #     return binascii.hexlify(test_f.read(2)) == b'1f8b'

class BamMerge:
    def __init__(self, *args, **kwargs):
        self.cli_args = kwargs.get('cli_args')
        self.process_cli_args()

    def process_cli_args(self):
        self.cell_tag = self.cli_args.cell_tag
        self.inputs = [entry.strip() for entry in self.cli_args.inputs.strip().split(',')]
        if self.cli_args.labels is None:
            self.labels = [range(len(self.ibams))]
        else:
            self.labels = [entry.strip() for entry in self.cli_args.labels.strip().split(',')]
        if self.cli_args.bcs is None:
            self.process_bc = False
        else:
            self.process_bc = True
            self.bcs = [entry.strip() for entry in self.cli_args.bcs.strip().split(',')]
        if self.cli_args.out is None:
            self.outfile = os.path.join(os.getcwd(), "out.bam")
        else:
            self.outfile = os.path.join(self.cli_args.out, "out.bam")
        if len(self.labels) != len(self.inputs):
            raise ValueError('Number of input filenames and number of labels do not match:\nInputs: %s\nLabels: %s', self.inputs, self.labels)
        if self.process_bc:
            if len(self.bcs) != len(self.inputs):
                raise ValueError('Number of input filenames and number of barcodes do not match:\nInputs: %s\nBarcodes: %s', self.inputs, self.bcs)
            self.outbcs = os.path.join(self.cli_args.out, "outbcs.tsv")
            self.bc_is_gz = [file_type(i)=="gz" for i in self.bcs]
            if checkEqual(self.bc_is_gz) is False:
                raise ValueError('Compression of barcodes file seems to be discrepent, consider unzipping all:\nBarcodes: %s', self.bcs)
            self.bc_is_gz = all(self.bc_is_gz)
        self.iter_total=len(self.inputs)

    def merge(self):
        self.mergeAlignments()
        if self.process_bc:
            self.mergeBarcodes()

    def mergeAlignments(self):
        bamtmp = pysam.AlignmentFile(self.inputs[0], 'rb')
        bamout = pysam.AlignmentFile(self.outfile,'wb', template=bamtmp)
        bamtmp.close()
        for ITER in range(self.iter_total):
            bam = pysam.AlignmentFile(self.inputs[ITER], 'rb')
            for read in bam:
                #print(read)
                try:
                    cb = read.get_tag(self.cell_tag)
                    #print(cb)
                except KeyError:
                    continue
                read.set_tag(self.cell_tag, self.labels[ITER]+cb, "Z")
                bamout.write(read)
            bam.close()
        bamout.close()

    def mergeBarcodes(self):
        with open(self.outbcs, 'w') as out_file:
            #tsv_writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\n')
            for ITER in range(self.iter_total):
                if self.bc_is_gz:
                    tsv_in = gzip.open(self.bcs[ITER], 'r')
                    for row in tsv_in:
                        newline = self.labels[ITER]+row.decode("utf-8")
                        #tsv_writer.writerow([newline])
                        out_file.writelines(newline)
                else:
                    tsv_in = open(self.bcs[ITER], 'r')
                    for row in tsv_in:
                        newline = self.labels[ITER]+row
                        #tsv_writer.writerow([newline])
                        out_file.writelines(newline)
                tsv_in.close()
            out_file.close()
            if self.bc_is_gz:
                with open(self.outbcs, 'rb') as f_in:
                    with gzip.open(str(self.outbcs +'.gz'), 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(self.outbcs)











