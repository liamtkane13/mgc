#!/usr/bin/env python3

# convert_pdf_to_csv_CA_CCC.py

import argparse 
import tabula

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input samtools idxstats output in TSV format for analysis')
	parser.add_argument('-i', '--infiles', help = 'PDF files to convert to CSVs', nargs = '+', required = True, dest = 'infiles')
	args = parser.parse_args()
	infiles = args.infiles
	return infiles

def convert_PDFs(files):
	
	for file in files:

		filename = file.split('.')[0]

		df = tabula.read_pdf(file, stream = True, pages = 1)

#		print(df)

		for i in df:
			print(i)

def main():

	infiles = parse_arguments()
	convert_PDFs(infiles)

if __name__ == '__main__':
	main()	