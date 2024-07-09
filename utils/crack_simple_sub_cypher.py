#!/usr/bin/env python3

import argparse

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input samtools idxstats output in TSV format for analysis')
	parser.add_argument('-i', '--infile', help = 'List of codes to crunch', required = True, dest = 'infile')
	parser.add_argument('-t', '--tsv', help = 'TSV of cypher in key-value format', required = True, dest = 'tsv')
	args = parser.parse_args()
	infile = args.infile
	tsv = args.tsv
	return infile, tsv

def crack_the_cypher(code_file, cypher_file):

	cypher_hash = {}

	print(f'PackageLabel\tDecodedLabel')

	with open(cypher_file, 'r') as cypher, open(code_file, 'r') as barcodes:

		for line in cypher:

			(c1, c2) = line.rstrip('\n').split('\t')

			cypher_hash[c1] = c2

		for line in barcodes:

			character_counter = 0
			
			barcode = line.rstrip('\n')

			decoded_barcode = '1A'


			for character in barcode:

				character_counter += 1

				new_character = cypher_hash[character]

				if character_counter <= 2:

					continue

				else:	

					decoded_barcode = decoded_barcode + new_character



			print(f'{barcode}\t{decoded_barcode}')	



def main():
	
	infile, tsv = parse_arguments()
	crack_the_cypher(infile, tsv)

if __name__ == '__main__':
	main()	