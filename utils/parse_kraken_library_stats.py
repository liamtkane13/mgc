#!/usr/bin/env python3

# parse_kraken_library_stats.py

import argparse
import pandas as pd

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the tsv file to produce a bar plot')
    parser.add_argument('-i', '--infile', help = 'Kraken "assembly summary" file for analysis', required = True, nargs = '+', dest = 'infile')
    args = parser.parse_args()
    infile = args.infile
    return infile

def parse_files(files):
	
	for file in files:

		file_name_raw = file.split("/")[-2]
		file_name = (f'{file_name_raw}_assembly_stats.tsv')
		df = pd.read_csv(file, sep = '\t', skiprows = 1) 
		stats = (df[['#assembly_accession', 'species_taxid', 'organism_name']])
		stats.to_csv(file_name, sep='\t') 

def main():
	
	infiles = parse_arguments()
	parse_files(infiles)		

if __name__ == '__main__':
	main()	