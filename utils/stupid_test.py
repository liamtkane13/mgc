#!/usr/bin/env python3

import argparse
import subprocess
import statistics
import glob
import csv 
from subprocess import Popen, PIPE

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input BAM files for samtools depth, to be output as a tsv file')
	parser.add_argument('-i', '--infiles', nargs = '+', help = 'BAM files for samtools', required = True, dest = 'infiles')
	parser.add_argument('-s', '--sample_sheet', help = 'Sample Sheet for naming', dest = 'sample_sheet')
	args = parser.parse_args()
	sample_sheet = args.sample_sheet
	matched_files = []
	for file in args.infiles:
		if glob.escape(file) != file:
			matched_files.extend(glob.glob(file))
		else:
			matched_files.append(file)
	return matched_files, sample_sheet	


def make_name_dictionary(samplesheet):
	name_dictionary = {}
	with open(samplesheet, 'r')	as file:
		reader = csv.reader(file)
		for line in reader:
			print(line)
		name_dictonary = {rows[3]:rows[0] for rows in reader}
		print(name_dictionary)

def main():
	matched_files, sample_sheet = parse_arguments()
	name_dictionary = make_name_dictionary(sample_sheet)

main()        
