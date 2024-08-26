#!/usr/bin/env python3

# combine_WA_lab_results_tsvs.py

import argparse
import pandas as pd 



def parse_arguments():
	parser = argparse.ArgumentParser(description='Input CSVs to combine')
	parser.add_argument('-i', '--infiles', help = 'CSVs to combine', nargs = '+', required = True, dest = 'infiles')
	parser.add_argument('-o', '--outfile_name', help = 'Name for output CSV', required = True, dest = 'outfile')
	args = parser.parse_args()
	infiles = args.infiles
	outfile = args.outfile
	return infiles, outfile 

def parse_and_combine_tsvs(files, outname):
	
	for file in files:

		with open(file, encoding="utf8", errors='ignore') as f:

			counter = 0

			for line in f:

				counter +=1

				if counter < 10:
					print(line)


			df = pd.read_csv(f, sep='\t')
			print(df)	
			
def main():
	
	infiles, outfile = parse_arguments()
	parse_and_combine_tsvs(infiles, outfile)

if __name__ == '__main__':
	main()					