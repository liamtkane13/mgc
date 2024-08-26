#!/usr/bin/env python3

import argparse
import pandas as pd
import datetime as dt 

def parse_arguments():

	parser = argparse.ArgumentParser(description='Input CSVs for conversion')
	parser.add_argument('-i', '--infiles', help = 'CSVs to convert', nargs = '+', required = True, dest = 'infiles')
	args = parser.parse_args()
	infiles = args.infiles

	return infiles


def convert_files(files):

	for file in files:

		filename = file.split('.')[0]
		outname = filename + 'FIXED_DATE.tsv'

		df = pd.read_csv(file)

		df['FinishedDate'] = (pd.to_datetime(df.FinishedDate, format='mixed')) #.dt.strftime('%Y-%m-%d')
#		df['FinishedDate'].dt.strftime('%Y-%m-%d')
		for i in df['FinishedDate']:

			if i != 'nan':

#				date = (str(i)).split(' ')[0]
#				print(date)
				df['FinishedDate'].dt.strftime('%Y-%m-%d')

			else:
				print(f'silly!')
				continue

	print(df['FinishedDate'])				



#		df.to_csv(outname, sep = '\t', header = True, index = False)	


def main():

	infiles = parse_arguments()
	convert_files(infiles)

if __name__ == '__main__':
	main()	