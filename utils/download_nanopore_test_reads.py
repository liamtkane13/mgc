#!/usr/bin/env python3

# download_nanopore_test_reads.py

import json
import subprocess


def make_download_file():

    ftp = []

    with open('filereport_read_run_PRJEB51164_json.txt') as file:
        for line in file:
            if 'r10.4' in line:
                split_line = line.split(',')
                for i in split_line:
                    if '"submitted_ftp"' in i:
                        ftp.append(str(i.split('"')[3]))
        return ftp

                   

def make_org_lists(ftp_links):

    ecoli_ftp = []
    klebsiella_ftp = []
    pseudo_ftp = []
    mrsa_ftp = []

    for i in ftp_links:

        if 'Ecoli' in i:
            ecoli_ftp.append(i)
           
        if 'Kpneumo' in i:
            klebsiella_ftp.append(i)

        if 'Pa01' in i:
            pseudo_ftp.append(i)
         
        if 'MRSA' in i:
            mrsa_ftp.append(i)
            
    


def main():
    ftp = make_download_file()
    make_org_lists(ftp)

if __name__ == '__main__':
    main()
