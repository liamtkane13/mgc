#!/usr/bin/env python3

# parse_qualimap_cov_tsv.py

import argparse
import pandas as pd
from subprocess import check_output as run 


def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the Qualimap derived Coverage TSV')
    parser.add_argument('-i', '--infile', help = 'Per Chromosome Coverage TSV', nargs = '+', required = True, dest = 'infile')
    parser.add_argument('-b', '--batch', help = 'Name of run or batch for output file', required = True, dest = 'batch')
    parser.add_argument('-p', '--path', help = 's3 path to BAM files', required = True, dest = 'path')
    args = parser.parse_args()
    infile = args.infile
    batch = args.batch
    path = args.path
    return infile, batch, path

def make_virus_dict():

    virus_dict = {} 
    with open('/home/ubuntu/liam/liam_git/utils/full_virus_names.txt', 'r') as file:
        for line in file:
            line = line.strip('\n')
            accession = line.split('|')[3]
            description = line.split('|')[4].lstrip(' ')
            virus_dict[accession] = description
    
    return virus_dict  


def produce_igv_links(pathy):
    
    ls_command = (f'aws s3 ls s3://mgcdata/{pathy}')
    ls_output = (run(['bash', '-c', ls_command])).decode('utf8').rstrip('\n')
    raw_output = ls_output.split(' ')

    bam_files = []
    counter = 0

    for i in raw_output:
        if 'bam' in i:
            if 'bai' in i:
                continue
            else:    
                bam = i.split('\n')[0]
            bam_files.append(bam)

    igv_link = "http://localhost:60151/load?file=" 

    for file in bam_files:
        counter += 1
        if counter == 1:
            file_link = (f'https://mgcdata.s3.amazonaws.com/{pathy}{file}')
        else:
            file_link = (f',https://mgcdata.s3.amazonaws.com/{pathy}{file}')
        igv_link = igv_link + file_link
    end_of_link = "&genome=https://mgcdata.s3.amazonaws.com/shared/ref/all-virus.fasta&locus="
    final_igv_link = igv_link + end_of_link 
    return final_igv_link


def tsv_crunching(files, batch, link, dicti):

    counter = 0

    for file in files:

        counter +=1

        if counter == 1:
            first_df = pd.read_csv(file, sep='\t')

        if counter == 2:
            second_df = pd.read_csv(file, sep='\t')
            final_df = pd.merge(first_df, second_df)

        if counter > 2:
            df = pd.read_csv(file, sep='\t')
            final_df = pd.merge(final_df, df)


    final_df['Virus_Description'] = final_df['Accession'].map(dicti)
    final_df['IGV_Link'] = link + final_df['Accession']        
  
    file_name = (f'{batch}_RNASeq_virus_mapping.tsv')
    final_df.to_csv(file_name, sep='\t')     


def main():
    infile_tsv, batch_name, s3_path = parse_arguments()
    virus_dict = make_virus_dict()
    igv_link = produce_igv_links(s3_path)
    tsv_crunching(infile_tsv, batch_name, igv_link, virus_dict)

if __name__ == '__main__':
	main()	    
