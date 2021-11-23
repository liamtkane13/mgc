#!/usr/bin/env python3

# 3d-dna-contig-to-scaffold-tsv.py

import argparse
import csv

parser = argparse.ArgumentParser(description='Open an assembly file and map contigs to HiC Scaffolds')
parser.add_argument('-i', '--infile', help='Assembly file to map', required=True,dest='infile')
args = parser.parse_args()

def parse_contigs():
    contig_list = []
    scaffold_list = []
    with open(args.infile, 'r') as infile:
        for line in infile:
            if line.startswith('>'):
                contig = line.strip('>')
                contigs = contig.split(' ')
                contig_list.append(contigs)
#            print(contig_list)
            for line in contig_list:
                contig_name = line[0]
                contig_number = line[1]
                contig_length = line[2]
            print(f'{contig_name}\t{contig_number}\t{contig_length}')

def main():
    parse_contigs()

if __name__ == '__main__':
    main()
