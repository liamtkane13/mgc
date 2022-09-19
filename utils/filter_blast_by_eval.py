#!/usr/bin/env python3

# filter_blast_by_eval.py

import sys
import argparse


parser = argparse.ArgumentParser(description='Open a BLAST output file, filter hits by maximum e-value and return requested number of hits')
parser.add_argument('-i', '--infiles', nargs = '+', help = 'BLAST file to query', required = True, dest = 'infiles')
parser.add_argument('-e', '--e_value', help = 'Maximum e-value to filter', required = True, dest = 'e_value')
parser.add_argument('-n', '--num_hits', help = 'Number of hits requested', required = True, dest = 'num_hits')
args = parser.parse_args()


def sort_key(list_name):
    return list_name[10]


def parse_blast_files(files, eval):
    
    blast_list = []
    query_id_list = []
    
    for file in files:
        with open(file, 'r') as file:

            for line in file:
                linecomp = line.split('\t')
                query_id = linecomp[0]
                e_val = linecomp[10]
                e_val = float(e_val)
                
                if query_id not in query_id_list:
                    query_id_list.append(query_id)

                if e_val < float(eval):
                    filtered_e_val = str(e_val)

                    if filtered_e_val in line:
                        blast_list.append(line)
            return blast_list, query_id_list



def sort_and_subsample_results(data_list1, data_list2, numhits):
    data_list1.sort(key = sort_key)
    top_hits_requested = data_list2[0:numhits]
#    for i in top_hits_requested:
#        print(i)
    for line in data_list1:
        for i in top_hits_requested:
            if i in line:
                print(line)





def main():
    infiles = args.infiles
    e_value = args.e_value
    num_hits = int(args.num_hits)
    blast_list, query_id_list = parse_blast_files(infiles, e_value)
    sort_and_subsample_results(blast_list, query_id_list, num_hits)
    

if __name__ == '__main__':
    main()
