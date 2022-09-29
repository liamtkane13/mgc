#!/usr/bin/env python3

from subprocess import check_output as run

def run_samtools_faidx(csvfile):
    with open(csvfile) as file:
        for line in file:
            contig = line.split(',')[0]
            start = line.split(',')[1]
            stop = line.split(',')[2]
            primer_set = line.split(',')[7]
            samtools_command = (f'samtools faidx /data/strainseek/ref/JL_female+Y-arrow-naming.fasta {contig}:{start}-{stop}')
            amplicon = run(['bash', '-c', samtools_command])
            print(f'{primer_set}\t{contig}\t{amplicon}\n')

def main():
#    csv_file = '/Users/liamkane/Desktop/Bioinformatics/photoperiod_amplicons.csv'
    csv_file = '/Dragen/Smart_photoperiod/photoperiod_amplicons.csv'
    run_samtools_faidx(csv_file)

if __name__ == "__main__":
    main()
