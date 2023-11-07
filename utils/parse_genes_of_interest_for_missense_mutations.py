#!/usr/bin/env python3

# parse_genes_of_interest_for_missense_mutations.py

import argparse
import csv
from subprocess import check_output as run 

def parse_arguments():

	parser = argparse.ArgumentParser(description='Input a list of genes and a VCF file to parse')
	parser.add_argument('-i', '--infile', help = 'List of genes', required = True, dest = 'infile')
	parser.add_argument('-v', '--vcf', help = 'VCF to parse', required = True, dest = 'vcf_file')
	args = parser.parse_args()
	infile = args.infile
	vcf_file = args.vcf_file
	return infile, vcf_file

def parse_variants(tsv, vcf):
	
	with open(tsv) as tsv:
		tsv_file = csv.reader(tsv, delimiter = '\t')
		for row in tsv_file:
			mRNA_id = row[5]
			coordinates = (f'{row[0]}:{row[1]}-{row[2]}')
			print(mRNA_id)
			print(coordinates)
			tabix_command = (f'tabix -p {coordinates} {vcf}')
			print(tabix_command)


def main():
	
	infile, vcf_file = parse_arguments()
	parse_variants(infile, vcf_file)

if __name__ == '__main__':
	main()					