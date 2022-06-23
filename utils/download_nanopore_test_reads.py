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
            
    return ecoli_ftp, klebsiella_ftp, pseudo_ftp, mrsa_ftp    




def file_transfer(list_1, list_2, list_3, list_4):

    for i in list_1:
        command_1 = (f'wget {i} -P /Dragen/ONT/NIHR-data/fastq/E-coli/')
        subprocess.check_output(['bash', '-c', command_1])
      
    for i in list_2:
        command_2 = (f'wget {i} -P /Dragen/ONT/NIHR-data/fastq/Klebsiella-pneumoniae/')
        subprocess.check_output(['bash', '-c', command_2])

    for i in list_3:
        command_3 = (f'wget {i} -P /Dragen/ONT/NIHR-data/fastq/Pseudomonas-aeruginosa-PAO1/')
        subprocess.check_output(['bash', '-c', command_3])

    for i in list_4:
        command_4 = (f'wget {i} -P /Dragen/ONT/NIHR-data/fastq/Staphylococcus-aureus-MRSA252/')
        subprocess.check_output(['bash', '-c', command_4])




def main():
    ftp = make_download_file()
    ecoli_ftp, klebsiella_ftp, pseudo_ftp, mrsa_ftp = make_org_lists(ftp)
    file_transfer(ecoli_ftp, klebsiella_ftp, pseudo_ftp, mrsa_ftp)

if __name__ == '__main__':
    main()
