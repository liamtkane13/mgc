#!/usr/bin/env python3

# count_MSA_mismatches.py

from Bio import AlignIO
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the MSA in FASTA Format')
    parser.add_argument('-i', '--infile', help = 'FASTA MSA to be read', required = True, dest = 'infile')
    args = parser.parse_args()
    MSA = args.infile
    return MSA


def read_and_score_MSA(infile):
	alignments = AlignIO.parse(open(infile), "fasta")
	gap_indicator = '-'
	mismatches = 0
#	length_of_alignment = [len(record) for record in alignments]
	for i in alignments:
		print(f"{i}")
		if gap_indicator in i:
			mismatches += 1
	print(mismatches)




def main():
	MSA = parse_arguments()
	read_and_score_MSA(MSA)

if __name__ == '__main__':
	main()	    