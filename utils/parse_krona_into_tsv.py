#!/usr/bin/env python3

# parse_krona_into_tsv.py

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the Qualimap derived Coverage TSV')
    parser.add_argument('-i', '--infile', help = 'krona plot to parse', nargs = '+', required = True, dest = 'infile')
    args = parser.parse_args()
    infile = args.infile
    return infile


def parse_html(file):
	my_dict = {}
	counter = 0
	for i in file:
		with open(i, 'r') as file:
			for it in file:
				if 'k2_pluspfp_16gb' in it:
					counter += 1
					sample_name = it.split('-')[0].split('>')[1]
					my_dict[sample_name] = {}
					print(f'{sample_name}\t{counter}')
				if 'node name=' in it:
					node_name = it.split('=')[1].split('"')[1] 
					counts = (next(file)) 
					split_counts = counts.split('val>')[1].rstrip('</')
					my_dict[sample_name][node_name] = split_counts	
	print(my_dict)



def main():
	infile = parse_arguments()
	parse_html(infile)

if __name__ == '__main__':
	main()				    