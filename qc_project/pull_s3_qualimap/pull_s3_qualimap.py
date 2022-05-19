#!/usr/bin/env python3

# pull_s3_qualimap.py

import os 
import subprocess
from subprocess import Popen, PIPE



def make_rsp_list():

    bam_list = []

    with open('public_bam_list.txt') as file:
        for line in file:
            if "bai" in line:
                continue
            else:
                bam_info = line.split(' ')
                for i in bam_info:
                    if "bam" in i:
                        it = i.strip('\n')
                        bam_list.append(it)
    return bam_list


def run_qualimap(sample_list):

    for i in sample_list:

        download_process = (f'aws s3 cp s3://mgcdata/SS2/bams/public/{i} .') 
        subprocess.check_output(['bash', '-c', download_process])

        i_name = i.split('.')[0]
        qualimap_process = (f'qualimap bamqc -bam {i} -outdir {i_name} -outformat HTML')
        subprocess.check_output(['bash', '-c', qualimap_process])

        delete_process = (f'rm {i}')
        subprocess.check_output(['bash', '-c', delete_process])

        


def main():
    bam_list = make_rsp_list()
    run_qualimap(bam_list)



if __name__ == "__main__":
    main()
