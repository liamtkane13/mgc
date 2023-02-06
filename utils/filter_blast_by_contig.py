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
	forward_list = []
	reverse_list = []
	probe_list = []
	final_list = []
	with open(in_file, 'r') as file:
		for line in file:
			primer = line.split('\t')[0]
			contig = line.split('\t')[1]
			e_val = line.split('\t')[10]
			if primer == 'F':
				forward_list.append(line)
			if primer == 'R':
				reverse_list.append(line)
			if primer == 'P':
				probe_list.append(line)
		print(primer)
		print(forward_list)
		print(probe_list)					


def main():
	infile = parse_arguments()
	filter_blast_results(infile)


if __name__ == "__main__":
	main()						