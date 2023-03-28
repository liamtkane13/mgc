#!/usr/bin/env python3

# parse_qualimap_cov_tsv.py

import argparse
import pandas as pd


def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the Qualimap derived Coverage TSV')
    parser.add_argument('-i', '--infile', help = 'Per Chromosome Coverage TSV', nargs = '+', required = True, dest = 'infile')
    parser.add_argument('-b', '--batch', help = 'Name of run or batch for output file', required = True, dest = 'batch')
    args = parser.parse_args()
    infile = args.infile
    batch = args.batch
    return infile, batch


def tsv_crunching(files, batch):
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
            new_df = pd.merge(first_df, df)
    final_df = pd.merge(first_df, new_df)    
    print(final_df)
    file_name = (f'{batch}_RNASeq_virus_mapping.tsv')
    final_df.to_csv(file_name, sep='\t')     


def main():
    infile_tsv, batch_name = parse_arguments()
    tsv_crunching(infile_tsv, batch_name)

if __name__ == '__main__':
	main()	    