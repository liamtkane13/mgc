#!/usr/bin/env python3

# combine_spreadsheets_variable_file_type.py

import argparse
import pandas as pd 



def parse_arguments():
	parser = argparse.ArgumentParser(description='Input CSVs to combine')
	parser.add_argument('-i', '--infiles', help = 'CSVs to combine', nargs = '+', required = True, dest = 'infiles')
	parser.add_argument('-o', '--outfile_name', help = 'Name for output CSV', required = True, dest = 'outfile')
	parser.add_argument('-f', '--file_type', help = 'CSV or TSV', required = True, dest = 'ftype')
	parser.add_argument('-of', '--outfile_type', help = 'CSV or TSV', required = False, dest = 'oftype')
	args = parser.parse_args()
	infiles = args.infiles
	outfile = args.outfile
	ftype = args.ftype
	oftype = args.oftype
	return infiles, outfile, ftype, oftype

def combine_csvs(files, outname, outtype):
	
	df = pd.concat(map(pd.read_csv, files), ignore_index = True)

	if outtype == 'tsv':

		outname = outname + '.tsv'
		df.to_csv(outname, header=True, index=False, sep = '\t')

	else:	

		outname = outname + '.csv'
		df.to_csv(outname, header=True, index=False)	

def combine_tsvs(files, outname, outtype):

	df = pd.concat([pd.read_csv(f, sep = '\t') for f in files])

	if outtype == 'tsv':

		outname = outname + '.tsv'
		df.to_csv(outname, header=True, index=False, sep = '\t')

	else:	

		outname = outname + '.csv'
		df.to_csv(outname, header=True, index=False)	


def combine_excel_files(files, outname, outtype):
	
	df = pd.concat([pd.read_excel(f) for f in files])

	
	if outtype == 'tsv':

		outname = outname + '.tsv'
		df.to_csv(outname, header=True, index=False, sep = '\t')

	else:	

		outname = outname + '.csv'
		df.to_csv(outname, header=True, index=False)


def combine_files(files, outname, fitype, outtype):
	
	if fitype == 'csv':

		combine_csvs(files, outname, outtype)

	if fitype == 'tsv':

		combine_tsvs(files, outname, outtype)	

	if fitype == 'excel':
		
		combine_excel_files(files, outname, outtype)	
			

def main():

	infiles, outfile, ftype, oftype = parse_arguments()
	combine_files(infiles, outfile, ftype, oftype)

if __name__ == '__main__':
	main()	