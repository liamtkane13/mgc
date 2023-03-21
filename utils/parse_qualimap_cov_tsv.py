#!/usr/bin/env python3

# parse_qualimap_cov_tsv.py

import argparse
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the Qualimap derived Coverage TSV')
    parser.add_argument('-i', '--infile', help = 'Per Chromosome Coverage TSV', nargs = '+', required = True, dest = 'infile')
    args = parser.parse_args()
    infile = args.infile
    return infile


def tsv_crunching(files):
    data = []
    counter = 0
    for file in files:
        counter +=1
        df = pd.read_csv(file, sep='\t')
        print(df)
        if counter == 1:
            data.append(df)
            first_df = pd.concat(data)
        else:
            final_df = pd.merge(first_df, df)
    print(final_df)          


def main():
    infile_tsv = parse_arguments()
    tsv_crunching(infile_tsv)

if __name__ == '__main__':
	main()	    