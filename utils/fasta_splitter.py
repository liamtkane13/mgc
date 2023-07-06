#!/usr/bin/env python3 

# fasta_splitter.py

import argparse
from Bio import SeqIO 

def parse_arguments():

	parser = argparse.ArgumentParser(description='Input the FASTA file to be split')
	parser.add_argument('-f', '--file', help = 'FASTA file to butcher', required = True, dest = 'infile')
	parser.add_argument('-t', '--tag', help = 'Tag of interest in Contig Description', required = False, dest = 'tag')
	args = parser.parse_args()
	infile = args.infile
	tag = args.tag 
	
	return infile, tag 


def split_fasta(file, tag):
	
	for record in SeqIO.parse(file, 'fasta'):
		
		accession_id = record.id + '.fasta'

		if tag is not None:

			if tag in record.description:

				with open(accession_id, 'w') as outfile:
					SeqIO.write(record, outfile, "fasta")			
				outfile.close()
			
			else:
				
				continue

		else:			

			with open(accession_id, 'w') as outfile:
				SeqIO.write(record, outfile, "fasta")			
			outfile.close()		


def main():
	
	infile, tag = parse_arguments()
	split_fasta(infile, tag)


if __name__ == '__main__':
	main()			