#!/usr/bin/env python3

# 3d-dna-contig-to-scaffold-tsv.py

import argparse
import csv

parser = argparse.ArgumentParser(description='Open an assembly file and map contigs to HiC Scaffolds')
parser.add_argument('-i', '--infile', help='Assembly file to map', required=True,dest='infile')
args = parser.parse_args()

contig_dict = {}
scaffold_list = []


def parse_contigs():
    counter = 0
    with open(args.infile, 'r') as infile:
        for lines in infile:
            line = lines.rstrip('\n')
            if line.startswith('>'):
                contig_array = line.strip('>').split(' ')
                name = contig_array[0]
                number = contig_array[1]
                length = contig_array[2]
                contig_dict[number] = name 
                
            else:
                scaffolds = line.split(' ')
                scaffold_list.append(scaffolds)
                counter +=1
    return counter

def align_scaffolds(dict, list):
    for item in list:
        if item in dict.keys():
            print(item)
    

def main():
    counter = parse_contigs()
#    print(contig_dict)
#    print(scaffold_list)
#    align_scaffolds(contig_dict, scaffold_list)
    print(counter)

if __name__ == '__main__':
    main()
