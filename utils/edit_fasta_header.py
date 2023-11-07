#!/usr/bin/env python3

# edit_fasta_header.py

import argparse
from Bio import SeqIO

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input the FASTA file to edit')
	parser.add_argument('-i', '--infile', help = 'FASTA to edit', required = True, dest = 'infile')
	parser.add_argument('-f', '--heady', help = 'FASTA header to add', required = True, dest = 'heady')
	args = parser.parse_args()
	infile = args.infile
	heady = args.heady
	return infile, heady

def edit_header(file, head):

	file_name_raw = file.split('/')[-1].split('.')[0]
	file_name = (f'{file_name_raw}_fixed_header.fasta')
	with open(file) as file, open(file_name, 'w') as outfile:
		records = SeqIO.parse(file, 'fasta')
		for record in records:
			original_id = record.id
			edited_id = (f'{original_id}|kraken:taxid|{head}')
			record.id = edited_id
			print(record.id)
			SeqIO.write(record, outfile, 'fasta')	

def main():
	
	infile, heady = parse_arguments()
	edit_header(infile, heady)

if __name__ == '__main__':
	main()				