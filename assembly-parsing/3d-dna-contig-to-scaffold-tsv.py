#!/usr/bin/env python3

# 3d-dna-contig-to-scaffold-tsv.py

import argparse
import csv

parser = argparse.ArgumentParser(description='Open an assembly file and map contigs to HiC Scaffolds')
parser.add_argument('-i', '--infile', help='Assembly file to map', required=True,dest='infile')
args = parser.parse_args()

contig_dict = {}

def parse_contigs():
    counter = 0
    with open(args.infile, 'r') as infile:
        for line in infile:
            if line.startswith('>'):
                contig_array = line.strip('>').split(' ')
                name = contig_array[0]
                number = contig_array[1]
                length = contig_array[2]
                contig_dict[number] = name 
                
            else:
                scaffolds = line.split(' ')
                counter +=1
#            print(scaffolds)
        return contig_dict



#def align_scaffolds():
#    with open(args.infile, 'r') as infile:

def main():
    parse_contigs()
    print(contig_dict)


if __name__ == '__main__':
    main()
