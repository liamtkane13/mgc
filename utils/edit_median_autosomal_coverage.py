#!/usr/bin/env python3

# edit_median_autosomal_coverage.py

import argparse
import json 

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input the JSON Files for correction')
	parser.add_argument('-i', '--infile', help = 'strainSEEK JSON file for correction', required = True, nargs = '+', dest = 'infile')
	args = parser.parse_args()
	infile = args.infile
	return infile


def edit_json(file):
	with open(file, 'w') as file:
		data = json.load(file)
		print(data['Median_autosomal_coverage'])




def main():
	infile = parse_arguments()
	edit_json(infile)

if __name__ == '__main__':
	main()		