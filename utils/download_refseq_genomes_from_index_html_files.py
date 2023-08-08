#!/usr/bin/env python3

# download_refseq_genomes_from_index_html_files.py

import argparse
from subprocess import check_output as run 

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input (a) FASTQ file(s) to filter')
    parser.add_argument('-i', '--infiles', help = 'FASTQ files to filter', required = True, nargs = '+', dest = 'infiles')
    args = parser.parse_args()
    infiles = args.infiles
    return infiles

def download_genomes(files):

	for file in files:
		with open(file, 'r') as file:
			for line in file:
				if "href" in line:
					link = line.split('"')[1]
#					print(link)
		download_command = (f'wget {link}/*fna.gz')
		print(download_command)
		run(['bash', '-c', download_command])	

def main():
	infiles = parse_arguments()
	download_genomes(infiles)

if __name__ == '__main__':
	main()						