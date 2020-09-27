#!/usr/bin/env python
import os
import sys
import pysam


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
            self.bcs = [entry.strip() for entry in self.cli_args.bcs.strip().split(',')]
        if self.cli_args.out is None:
            self.outfile = os.path.join(os.getcwd(), "out.bam")
        else:
            self.outfile = os.path.join(self.cli_args.out, "out.bam")
        if len(self.labels) != len(self.inputs):
            raise ValueError('Number of input filenames and number of labels do not match:\nInputs: %s\nLabels: %s', self.inputs, self.labels)
        if self.process_bc:
            if len(self.bcs) != len(self.inputs):
                raise ValueError('Number of input filenames and number of barcodes do not match:\nInputs: %s\nBarcodes: %s', self.inputs, self.labels)
        self.iter_total=len(self.inputs)

    def merge(self):
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
