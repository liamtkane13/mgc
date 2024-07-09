#!/usr/bin/env python3

import argparse
import pandas as pd

def parse_arguments():

	parser = argparse.ArgumentParser(description='Input samtools idxstats output in TSV format for analysis')
	parser.add_argument('-t1', '--tsv_1', help = 'TSV 1 to join', required = True, dest = 'tsv_1')
	parser.add_argument('-t2', '--tsv_2', help = 'TSV 2 to join', required = True, dest = 'tsv_2')
	parser.add_argument('-c', '--column', help = 'Column on which to join the TSVs', required = True, dest = 'column')
	parser.add_argument('-o', '--outfile', help = 'Name of outfile for joined TSVs', required = True, dest = 'outfile')
	args = parser.parse_args()
	tsv_1 = args.tsv_1
	tsv_2 = args.tsv_2
	column = args.column
	outfile = args.outfile

	return tsv_1, tsv_2, column, outfile

def join_tsvs(file1, file2, col, out):

	file1_df = pd.read_csv(file1, sep='\t')
	file2_df = pd.read_csv(file2, sep='\t')

	new_df = pd.merge(file1_df, file2_df, on = [col])

	new_df.to_csv(out, sep='\t', header=True, index=False)	

def main():
	
	tsv_1, tsv_2, column, outfile = parse_arguments()
	join_tsvs(tsv_1, tsv_2, column, outfile)

if __name__ == '__main__':
	main()	