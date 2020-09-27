[![PyPI](https://img.shields.io/pypi/v/simplesam.svg?)](https://pypi.org/project/piperna/)
<!-- [![Build Status](https://travis-ci.org/mdshw5/simplesam.svg?branch=master)](https://travis-ci.org/mdshw5/simplesam) -->
[![Documentation Status](https://readthedocs.org/projects/piperna/badge/?version=latest)](https://piperna.readthedocs.io/en/latest/?badge=latest)

# piperna
==========

version 0.5

A python wrapper for processing of bulk RNA seq data

## Requirements

1. Python > 3.5 (piperna uses the 'six' package but will attempt to install if not already installed)
2. Computing cluster with PBS or SLURM
3. Modules installed for python, STAR or kallisto, 
4. R Modules for GenomicAlignments, rtracklayer, and Rsamtools if running SUMMARIZE

## Installation

Installation can probably be done correctly many different ways.  Here are the methods that have worked for us.  We recommend that piperna be installed with pipx.

**At SCRI do the following**
```bash
module load python
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install --include-deps --pip-args '--trusted-host pypi.org --trusted-host files.pythonhosted.org' piperna
```


**At the FHCRC do the following...**
```bash
module load Python/3.6.7-foss-2016b-fh1
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install --include-deps piperna
```

You should then be able to test installation by calling piperna.  After running the folllowing, you should see the help screen displayed.

```bash
piperna
```



## Usage

```bash
piperna usage: A wrapper for running RNASeq Alignment [-h]
                                              [--fastq_folder FASTQ_FOLDER]
                                              [--genome_key GENOME_KEY]
                                              [--sample_flag SAMPLE_FLAG]
                                              [--runsheet RUNSHEET]
                                              [--typeofseq {single,pe}]
                                              [--software {STAR,kallisto}]
                                              [--output OUTPUT] [--debug]
                                              [--cluster {PBS,SLURM}]
                                              [--user USER]
                                              [--threads THREADS] [--mfl MFL]
                                              [--sfl SFL] [--count]
                                              [--outSAMtype OUTSAMTYPE]
                                              [--addSTARstring ADDSTARSTRING]
                                              [--log_prefix LOG_PREFIX]
                                              [--verbose]
                                              {MAKERUNSHEET,ALIGN,SUMMARIZE}

positional arguments:
  {MAKERUNSHEET,ALIGN,SUMMARIZE}
                        a required string denoting segment of pipeline to run.
                        1) "MAKERUNSHEET" - to parse a folder of fastqs; 2)
                        "ALIGN" - to perform alignment; 3) "SUMMARIZE" - to
                        summarize and count reads

optional arguments:
  -h, --help            show this help message and exit
  --fastq_folder FASTQ_FOLDER, -fq FASTQ_FOLDER
                        For MAKERUNSHEET only: Pathname of fastq folder (files
                        must be organized in folders named by sample)
  --genome_key GENOME_KEY, -gk GENOME_KEY
                        For MAKERUNSHEET only: abbreviation to use "installed"
                        genomes in the runsheet (See README.md for more
                        details
  --sample_flag SAMPLE_FLAG, -f SAMPLE_FLAG
                        FOR MAKERUNSHEET only string to identify samples of
                        interest in a fastq folder
  --runsheet RUNSHEET, -r RUNSHEET
                        tab-delim file with sample fields as defined in the
                        script. - REQUIRED for all jobs except MAKERUNSHEET
  --typeofseq {single,pe}, -t {single,pe}
                        Type of sequencing performed - REQUIRED for
                        MAKERUNSHEET
  --software {STAR,kallisto}, -s {STAR,kallisto}
                        To set desired software, required and used for
                        MAKERUNSHEET only
  --output OUTPUT, -o OUTPUT
                        To set output path, required for MAKERUNSHEET
  --debug, -d           To print commands (For testing flow)
  --cluster {PBS,SLURM}, -c {PBS,SLURM}
                        Cluster software. OPTIONAL Currently supported: PBS
                        and SLURM
  --user USER, -u USER  user for submitting jobs - defaults to username.
                        OPTIONAL
  --threads THREADS, -th THREADS
                        To set number of cores
  --mfl MFL, -mf MFL    Mean fragment length (kallisto ONLY)
  --sfl SFL, -sf SFL    SD fragment length (kallisto ONLY)
  --count, -co          Run Count (STAR Only)
  --outSAMtype OUTSAMTYPE, -st OUTSAMTYPE
                        To define type of SAM/BAM output (STAR Only)
  --addSTARstring ADDSTARSTRING, -a ADDSTARSTRING
                        Additional STAR arguments to be run on all jobs in
                        runsheet (STAR Only)
  --log_prefix LOG_PREFIX, -l LOG_PREFIX
                        Prefix specifying log files for henipipe output from
                        henipipe calls. OPTIONAL
  --verbose, -v         Run with some additional ouput - not much though...
                        OPTIONAL
```


## Runsheet

The runsheet is the brains of the piperna workflow.  You can make a runsheet using the MAKERUNSHEET command.  This command will parse a directory of fastq folder (specified using the -fq flag; fastq files should be organized in subfolders named by sample) and will find fastq mates (R1 and R2 - Currently only PE sequencing is supported).  Running piperna MAKERUNSHEET will find and pair these fastqs for you and populate the runsheet with genome index locations (see below) and output filenames with locations as specified using the -o flag.  Note that piperna output will default to the current working directory if no location is otherwise specified.  There is an option for selecting only folders that contain a specific string (using the -sf flag).  *After generation of a runsheet (csv file), you should take a look at it in Excel or Numbers to make sure things look okay...*  Here are the columns that you can include.  Order is irrelevant.  Column names (headers) exactly as written below are required.

### Example Runsheet 

**absolute pathnames are required for runsheets**

| sample | index | fastq1 | fastq2 | output |  software  |     gtf    |
|--------|-------|--------|--------|--------|------------|------------|
|  mys1  |  path |  path  |  path  |  path  |   STAR     |    path    |
|  mys2  |  path |  path  |  path  |  path  |   STAR     |    path    |


* 'sample' name of the sample REQUIRED.  
* 'index' location of the indexed fasta file REQUIRED.  
* 'fastq1' a tab seperated string of filenames denoting location of all R1 files for a sample REQUIRED if paired end.  
* 'fastq2' a tab seperated string of filenames denoting location of all R2 files for a sample REQUIRED if paired end.  
* 'fastqs' a tab seperated string of filenames can be used for single end reads REQUIRED if single end.  
* 'output' name of the location for the aligned and sorted bam file.  
* 'software' either 'STAR' or 'kallisto'.  REQUIRED
* 'gtf' a location for annotation file in gtf format.  REQUIRED for SUMMARIZE.  

## Genomes and adding genome locations

you should have a previously indexed (by the software package of your choosing) location of your genome accessible to piperna.  This location is referred to in piperna as the 'index'.

piperna provides an easy way to add these locations to your system for repeated use using the --genome_key (-gk) option during MAKERUNSHEET commands.  A file called genomes.json can be found in the 'data' directory of the piperna install folder.  This file can be edited to include those locations you want to regularly put in the runsheet.  The following shows an example of a genomes.json file.  The files "top level" is a name that can be used in the --genome_key field (-gk) during runsheet generation to populate the columns of the runsheet with locations associated with that genome_key.  The 'default' key will be used when no genome_key is specified.

```json
{
    "default": {
      "index": "/path/path/hg38/STAR_index",
      "gtf": "/path/path/hg38/hg38.gtf"
    },
    "default_kallisto": {
        "index": "/path/path/hg38/kallisto_index",
        "gtf": "/path/path/hg38/hg38.gtf"
    }
}
```

## Doing a piperna run

Say your fastqs live within within subfolders of a folder 'fastq' in the folder 'data'.  So if you were to...
```bash
cd /data/fastq
ls
```
... you'd get a bunch of folders, each of which would be filled with fastqs.  Each folder name should correspond to a sample name.


**To run piperna, do the following...**
1. Make a new output directory 'piperna'.
2. Go into that directory and make a runsheet pointing to the fastq folder i.e. the folder level above.  (at the command line, piperna is cool with either relative or absolute pathnames; but as stated earlier, absolute pathnames are required for the runsheet.)
3.  Optionally you can only select directories of fastq files that contain in their name the string denoted using the -sf flag.
4. After inspecting and completing the runsheet, run ALIGN, NORM, and SEACR.  
5. Sit back have a cocktail.

```bash
cd ..
mkdir piperna
cd piperna
piperna MAKERUNSHEET -fq ../fastq -sf MySampleDirectoriesStartWithThisString -o .
piperna ALIGN -r runsheet.csv
piperna SUMMARIZE -r runsheet.csv -o SummarizedExperiment.RDS
```


## Interfacing with DESeq2

**After running piperna, the SummarizedExperiment.RDS file can be input directly into DESeq2 like this**

```R

```


## Acknowledgements

Written by Scott Furlan with code inspiration from Andrew Hill's cellwrapper.