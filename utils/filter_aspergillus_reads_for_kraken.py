#!/usr/bin/env python3

# filter_aspergillus_reads_for_kraken.py

from subprocess import check_output as run
import argparse
from Bio import SeqIO

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input (a) FASTQ file(s) to filter')
    parser.add_argument('-i', '--infiles', help = 'FASTQ files to filter', required = True, nargs = '+', dest = 'infiles')
    parser.add_argument('-l', '--length', help = 'Minimum length for filter', required = False, dest = 'length')
    parser.add_argument('-q', '--quality', help = 'Minimum quality for filter', required = False, dest = 'quality')
    args = parser.parse_args()
    infiles = args.infiles
    length = args.length
    quality = args.quality
    return infiles, length, quality

def filter_fastqs(files, length, qual):

	for file in files:

		file_name = file.split('.')[0]

		filtered_seqs = []

		for rec in SeqIO.parse(file, 'fastq'):

			if qual != None and length != None:
				
				qual = int(qual)
				length = int(length)
				
				if min(rec.letter_annotations["phred_quality"]) >= qual and len(rec.seq) >= length:
					print(rec)
					filtered_seqs.append(rec)
					output_file = (f'{file_name}_filtered_by_{length}_length_{qual}_quality.fastq')


			elif qual != None and length == None:

				qual = int(qual)

				if min(rec.letter_annotations["phred_quality"]) >= qual:
					print(rec)	
					filtered_seqs.append(rec)
					output_file = (f'{file_name}_filtered_by_{qual}_quality.fastq')


			elif length != None and qual == None:

				length = int(length)

				if len(rec.seq) >= length:
					print(rec)	
					filtered_seqs.append(rec)
					output_file = (f'{file_name}_filtered_by_{length}_length.fastq')

		SeqIO.write(filtered_seqs, output_file, "fastq")	
						

def main():
	fastqs, min_length, min_quality = parse_arguments()
	filter_fastqs(fastqs, min_length, min_quality)

if __name__ == '__main__':
	main()	