#!/usr/bin/env python3

# filter_blast_by_eval.py

import sys
import argparse


parser = argparse.ArgumentParser(description='Open a BLAST output file, filter hits by maximum e-value and return requested number of hits')
parser.add_argument('-i', '--infiles', nargs = '+', help = 'BLAST file to query', required = True, dest = 'infiles')
parser.add_argument('-e', '--e_value', help = 'Maximum e-value to filter', required = True, dest = 'e_value')
parser.add_argument('-n', '--num_hits', help = 'Number of hits requested', required = True, dest = 'num_hits')
args = parser.parse_args()

def parse_blast_files(files, eval, numhits):
    blast_list = []
    evals_list = []
    for file in files:
        with open(file, 'r') as file:
            for line in file:
                linecomp = line.split('\t')
                blast_list.append(linecomp)
                e_val = linecomp[10]
                e_val = float(e_val)
                if e_val < float(eval):
                    print(e_val)


def main():
    infiles = args.infiles
    e_value = args.e_value
    num_hits = args.num_hits
    parse_blast_files(infiles, e_value, num_hits)

if __name__ == '__main__':
    main()
