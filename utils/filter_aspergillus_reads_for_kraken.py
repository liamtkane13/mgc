#!/usr/bin/env python3

# filter_aspergillus_reads_for_kraken.py

from subprocess import check_output as run
import argparse
from Bio import SeqIO

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input (a) FASTQ file(s) to filter')
    parser.add_argument('-i', '--infiles', help = 'FASTQ files to filter', required = True, nargs = +, dest = 'infiles')
    parser.add_argument('-l', '--length', help = 'Minimum length for filter', required = False, dest = 'infiles')
    parser.add_argument('-q', '--quality', help = 'Minimum quality for filter', required = False, dest = 'infiles')
    args = parser.parse_args()
    infiles = args.infiles
    length = args.length
    quality = args.quality
    return infiles, length, quality

def filter_fastqs(files, len, qual):

	qual = int(qual)

	for file in files:
		for rec in SeqIO.parse(file, 'fastq'):
			if min(rec.letter_annotations["phred_quality"]) >= qual:
				print(rec)	

def main():
	fastqs, min_length, min_quality = parse_arguments()
	filter_fastqs(fastqs, min_length, min_quality)

if __name__ == '__main__':
	main()	