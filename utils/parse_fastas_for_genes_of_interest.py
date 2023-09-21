#!/usr/bin/eny python3

import argparse 
from Bio import SeqIO

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input (a) FASTA file(s) to filter')
    parser.add_argument('-i', '--infiles', help = 'FASTA files to filter', required = True, nargs = '+', dest = 'infiles')
    parser.add_argument('-g', '--gene', help = 'Gene to query from FASTAs', required = True, dest = 'gene')
    args = parser.parse_args()
    infiles = args.infiles
    gene = args.gene 
    return infiles, gene

def parse_fastas(files, gene_name):

	gene_of_interest = []
	outfile = (f'{gene_name}_seqs.fasta')

	for file in files:

		for rec in SeqIO.parse(file, 'fasta'):

			if gene_name in rec.description:
				gene_of_interest.append(rec)
	
	SeqIO.write(gene_of_interest, outfile, 'fasta')		


def main():
	
	infiles, gene = parse_arguments()
	parse_fastas(infiles, gene)

if __name__ == '__main__':
	main()						