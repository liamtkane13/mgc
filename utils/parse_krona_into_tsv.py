#!/usr/bin/env python3

# parse_krona_into_tsv.py

import argparse
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the Qualimap derived Coverage TSV')
    parser.add_argument('-i', '--infile', help = 'krona plot to parse', nargs = '+', required = True, dest = 'infile')
    parser.add_argument('-o', '--outfile', help = 'name of file to write to', required = True, dest = 'outfile')
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    return infile, outfile


def parse_html(file, out):
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

	df = pd.DataFrame.from_dict(my_dict, orient='columns')	
	out_name = (f'{out}_kraken_abundances.tsv')
	df.to_csv(out_name, sep='\t', header=True, index=True)




def main():
	infile, outfile = parse_arguments()
	parse_html(infile, outfile)

if __name__ == '__main__':
	main()				    