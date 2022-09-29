#!/usr/bin/env python3

from subprocess import check_output as run
import glob


def rename_files(files):
    for file in files:
        
        sample_name = file.split('/')[-1].split('_')[0]
        suffix = file.split('/')[-1].split('_')[1]
    
        if '1' in suffix:
            command_1 = (f'mv {file} {sample_name}_R1_001.fastq')
            run(['bash', '-c', command_1])
        if '2' in suffix:
            command_2 = (f' mv {file} {sample_name}_R2_001.fastq')
            run(['bash', '-c', command_2])

def main():
    infiles = '/Dragen/Smart_photoperiod/Smart_photosensitive/*fastq'
    infiles = glob.glob(infiles)
    rename_files(infiles)
   
if __name__ == "__main__":
    main()
