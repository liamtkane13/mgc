#!/usr/bin/env python3

# remove_Ns_from_fasta.py

import argparse
from Bio import SeqIO

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the FASTA to remove Ns and split')
    parser.add_argument('-i', '--infile', help = 'FASTA to split', required = True, dest = 'infile')
    args = parser.parse_args()
    infile = args.infile
    return infile  



def remove_ns_and_split(file):

	for record in SeqIO.parse(file, 'fasta'):

#		print(record.id)

		chunk = 0

		seq_elements = record.seq.split('N')

		for i in seq_elements:

			if 'A' in i:
				chunk += 1
				print(f'>{record.id} chunk {chunk}')
				print(i)



def main():
	
	infile = parse_arguments()
	remove_ns_and_split(infile)		

if __name__ == '__main__':
	main()	