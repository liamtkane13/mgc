#!/usr/bin/env python3

# psilocybe_variants_per_chromosome.py

import os
import glob
import subprocess
from subprocess import Popen, PIPE
import pandas as pd

def make_chromosome_dictionary():
    chromosome_dictionary = {
            'CM038998.1' : 'Chromosome 1',
            'CM038999.1' : 'Chromosome 2',
            'CM039000.1' : 'Chromosome 3',
            'CM039001.1' : 'Chromosome 4',
            'CM039002.1' : 'Chromosome 5',
            'CM039003.1' : 'Chromosome 6',
            'CM039004.1' : 'Chromosome 7',
            'CM039005.1' : 'Chromosome 8',
            'CM039006.1' : 'Chromosome 9',
            'CM039007.1' : 'Chromosome 10',
            'CM039008.1' : 'Chromosome 11',
            'CM039009.1' : 'Chromosome 12',
            'CM039010.1' : 'Chromosome 13',
            'JAFIQS020000014.1' : 'contig 1',
            'JAFIQS020000016.1' : 'contig 2',
            'JAFIQS020000017.1' : 'contig 3',
            'JAFIQS020000018.1' : 'contig 4',
            'JAFIQS020000019.1' : 'contig 5',
            'JAFIQS020000020.1' : 'contig 6',
            'JAFIQS020000021.1' : 'contig 7',
            'CM029846.1' : 'Mitochondrion'
    }
    return chromosome_dictionary

def tabix(ref_file, vcf_file, chrom_dict):
    process_chr = Popen(['tabix', '-l', ref_file], stdout=PIPE)
    variant_count_dict = {}
    chr_number = []

    for line in process_chr.stdout:
        chr_number.append(line.decode('utf8').rstrip('\n'))
    
    for i in vcf_file:
        process_sample = Popen(['bcftools', 'query', '-l', i], stdout=PIPE)

        for num in chr_number:
            process_var = (f'tabix {i} {num} | wc -l')
            num_var = int(subprocess.check_output(['bash', '-c', process_var]).strip())
            chr_name = chrom_dict[num]

            for it in process_sample.stdout:
                sample_name = it.decode('utf8').rstrip('\n')
                if sample_name not in variant_count_dict:
                    variant_count_dict[sample_name] = {}

            variant_count_dict[sample_name][chr_name] = num_var 
    return variant_count_dict


def print_output(var_dict):
    data = pd.DataFrame(var_dict)
    data = data.fillna("-")
    data.to_csv("./psilocybe_variants_per_chromosome.csv", sep = "\t")




def main():
    reference_file = '/Juicer/shroomapedia/6-shrooms-02-17-2022/out/snpEff/snps-snpEff/all/PSP10018-filtered.vcf.snpEff.ann.vcf.gz'
    vcf_files = '/Juicer/shroomapedia/6-shrooms-02-17-2022/out/snpEff/snps-snpEff/all/*vcf.gz'
    vcf_files = glob.glob(vcf_files)
    chromosome_dictionary = make_chromosome_dictionary()
    variant_count_dict = tabix(reference_file, vcf_files, chromosome_dictionary)
    print_output(variant_count_dict)
    

if __name__ == '__main__':
    main()
