#!/usr/bin/env python3

import sys
import argparse

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input BLAST output file, to be filtered by best hit per contig')
	parser.add_argument('-i', '--infile', help = 'BLAST file to query', required = True, dest = 'infile')
	args = parser.parse_args()
	infile = args.infile
	return infile

def filter_blast_results(in_file):
	with open(in_file, 'r') as file:
		for line in file:
			print(line)


def main():
	infile = parse_arguments()
	filter_blast_results(infile)


if __name__ == "__main__":
	main()						