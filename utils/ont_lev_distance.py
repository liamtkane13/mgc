#!/usr/bin/env python3

# ont_lev_distance.py

import argparse
from Levenshtein import distance as lev

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input the Reference and Query Sequences in FASTA Format')
	parser.add_argument('-r', '--reference', help = 'Reference Sequence in FASTA Format', required = True, dest = 'reference')
	parser.add_argument('-q', '--query', help = 'Query Sequence in FASTA Format', required = True, dest = 'query')
	args = parser.parse_args()
	reference = args.reference
	query = args.query
	return reference, query

def calculate_ld(ref, que):
	with open(ref, 'r') as file1:
		for line in file1:
			if '>' in line:
				continue
			else:
				ref_seq = line
				print(f'ref: {ref_seq}')
		return ref_seq
	with open(que, 'r') as file2:
		for i in file2:
			if '>' in i:
				continue
			else:
				query_seq = i
		print(f'query: {query_seq}')
		return query_seq
	print(lev(ref_seq, query_seq))										

def main():
	reference, query = parse_arguments()
	calculate_ld(reference, query)

if __name__ == '__main__':
	main()	