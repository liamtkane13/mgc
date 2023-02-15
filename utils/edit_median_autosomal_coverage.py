#!/usr/bin/env python3

# edit_median_autosomal_coverage.py

import argparse
import json
import os 

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input the JSON Files for correction')
	parser.add_argument('-i', '--infile', help = 'strainSEEK JSON file for correction', required = True, nargs = '+', dest = 'infile')
	args = parser.parse_args()
	infile = args.infile
	return infile


def edit_json(files):
	for file in files:
		with open(file, 'r') as infile:
			data = json.load(infile)
			data["align_metrics_detail"]["Median_autosomal_coverage"] = '0.0'
			os.remove(file)
		with open(file, 'w') as new_file:
			json.dump(data, new_file)
			new_file.close()	



def sanity_check(filer):
	for i in filer:
		with open(i, 'r+') as file:
			data = json.load(file)
			print(data["align_metrics_detail"]["Median_autosomal_coverage"])



def main():
	infile = parse_arguments()
	edit_json(infile)
#	sanity_check(infile)

if __name__ == '__main__':
	main()		