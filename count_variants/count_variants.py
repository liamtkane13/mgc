#!/usr/bin/env python3

# count_variants.py

import argparse
import csv

parser = argparse.ArgumentParser(description="Open a TSV of Variants and count the number of variants and genotypes.")
parser.add_argument('-i', '--infile', help='TSV of variants to count', required=True)
args = parser.parse_args()

def count_variants():

    ho_counter = 0
    het_counter = 0
    
    with open(args.infile, 'r') as infile:
        file = csv.reader(infile, delimiter = "\t")

        for line in file:
            scaffold = line[0]
            variant = line[2]
            genotype = line[3]

            if genotype == '0/1':
                het_counter += 1
            
            if genotype == '1/1':
                ho_counter += 1
 
        print(f'\nNumber of homozygous variants: {ho_counter}')
        print(f'\nNumber of heterozygous variants: {het_counter}\n')

def main():
    count_variants()

if __name__ == "__main__":
    main()
