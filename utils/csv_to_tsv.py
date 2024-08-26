#!/usr/bin/env python3

# csv_to_tsv.py
# To anyone reading this, I'm sorry for writing such a simple silly script

import argparse
import pandas as pd 

def parse_arguments():

	parser = argparse.ArgumentParser(description='Input CSVs for conversion')
	parser.add_argument('-i', '--infiles', help = 'CSVs to convert', nargs = '+', required = True, dest = 'infiles')
	args = parser.parse_args()
	infiles = args.infiles

	return infiles

def convert_files(files):
	
	for file in files:

		filename = file.split('.')[0]
		outname = filename + '.tsv'

		df = pd.read_csv(file)

		df.to_csv(outname, sep = '\t', header = True, index = False)

			
	
def main():
	
	infiles = parse_arguments()
	convert_files(infiles)

if __name__ == '__main__':
	main()				