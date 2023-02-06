#!/usr/bin/env python3

# shroom_multi_ref_mapping_stats.py

import glob

infile = glob.glob('*.flagstat.txt')

def make_dictionaries():
    genome_dictionary = {
            'Psicy2_genomic' : 'Psilocybe cyanescens',
            'Psiser1_AssemblyScaffolds_Repeatmasked' : 'Psilocybe serbica'
            }
    strain_dictionary = {
            'PSP10007' : 'OR-Coast-3-SW',
            'PSP10051' : 'Tampa-2-SW',
            'PSP10050' : 'Tampa-1-SW',
            'PSP10076' : 'P-Mexicana-Galindoi-1-Mush',
            'PSP10052' : 'Tampa-3-SW',
            'PSP10038' : 'Malabar-2-PS',
            'PSP10037' : 'Malabar-1-PS',
            'PSP10036' : 'Malabar-3-PS'
            }
    return genome_dictionary, strain_dictionary

def parse_data(file, g_dict, s_dict):
    total = 'total'
    mapped = 'mapped ('
    with open(file, 'r') as file:
        for line in file:
            if total in line:
                total_reads = int(line.split(' ', 1)[0])
            if mapped in line:
                mapped_reads = int(line.split(' ', 1)[0])
        name = str(file)        
        psp = name.split('-', 1)[0].split("='", 1)[1]
        strain = s_dict[psp]
        genome_raw = name.split('-', 1)[1].split('.', 1)[0]
        genome = g_dict[genome_raw]
        percent_mapped = round(float((mapped_reads / total_reads) * 100), 2)
        print(f'\nSample: {strain}')
        print(f'\nGenome: {genome}')
        print(f'\nNumber of total reads: {total_reads}')
        print(f'\nNumber of mapped reads: {mapped_reads}')
        print(f'\nPercent mapped: {percent_mapped}%\n')

def main():
    genome_dictionary, strain_dictionary = make_dictionaries()
    for file in infile:
        file = str(file)
        parse_data(file, genome_dictionary, strain_dictionary) 

if __name__ == "__main__":
    main()
