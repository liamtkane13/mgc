#!/usr/bin/env python3

# 3d-dna-contig-to-scaffold-tsv.py

import argparse
import csv

parser = argparse.ArgumentParser(description='Open an assembly file and map contigs to HiC Scaffolds')
parser.add_argument('-i', '--infile', help='Assembly file to map', required=True,dest='infile')
args = parser.parse_args()

def parse_contigs():
    scaffold_list = []
    contig_dict = {}
    contig_length = {}
    with open(args.infile, 'r') as infile:
        for lines in infile:
            line = lines.rstrip('\n')
            if line.startswith('>'):
                contig_array = line.strip('>').split(' ')
                name = contig_array[0]
                number = int(contig_array[1])
                length = int(contig_array[2])
                contig_dict[number] = name
                contig_length[number] = length
            else:
                scaffolds = line.split(' ')
                scaffolds = list(map(int, scaffolds)) #turn list into list of integers from list of strings
                scaffold_list.append(scaffolds)
    return contig_dict, contig_length, scaffold_list

def align_scaffolds(contig_dict, contig_length, list):
    scaffold_number = 0
    for l in list:
        scaffold_number += 1
        scaffold_name = "%s_%s"%('HiC_scaffold', scaffold_number)
        for c in l:
            contig_name = contig_dict[abs(c)]
            strand = '+'
            if c < 0:
                strand = '-'
            print("%s\t%s\t%s\t%s"%(scaffold_name, contig_name, strand, contig_length[abs(c)]))
    

def main():
    contig_dict, contig_length, scaffold_list = parse_contigs()
    align_scaffolds(contig_dict, contig_length, scaffold_list)

if __name__ == '__main__':
    main()
