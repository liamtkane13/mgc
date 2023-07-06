#!/usr/bin/env python3 

# fasta_splitter.py

import argparse
from Bio import SeqIO 

def parse_arguments():

	parser = argparse.ArgumentParser(description='Input the FASTA file to be split')
	parser.add_argument('-f', '--file', help = 'FASTA file to butcher', required = True, dest = 'infile')
	args = parser.parse_args()
	infile = args.infile 
	
	return infile


def split_fasta(file):
	
	for record in SeqIO.parse(file, 'fasta'):
		print(record.id)


def main():
	
	infile = parse_arguments()
	split_fasta(infile)


if __name__ == '__main__':
	main()			