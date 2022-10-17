#!/usr/bin/env python3

import argparse
import subprocess 
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description='Input BAM files for samtools depth, to be output as a tsv file')
parser.add_argument('-i', '--infiles', nargs = '+', help = 'BAM files for samtools', required = True, dest = 'infiles')
args = parser.parse_args()

def make_name_dictionary():
	name_dictionary = {
		'barcode28' : 'MGC_A1_ITS',
		'barcode33' : 'MGC_C1_ITS',
		'barcode34' : 'D1_Direct_ITS',
		'barcode35' : 'D2_Direct_ITS',
		'barcode37' : 'D3_Direct_ITS',
		'barcode38' : 'D4_Direct_ITS',
		'barcode39' : 'MGC_A1_ROCK',
		'barcode40' : 'MGC_C1_ROCK',
		'barcode41' : 'D1_Direct_ROCK',
		'barcode42' : 'D2_Direct_ROCK',
		'barcode43' : 'D3_Direct_ROCK',
		'barcode44' : 'D4_Direct_ROCK'
	}
	return name_dictionary

def run_samtools(files, dictionary):

	for file in files:

		overall = 0
		cov_10 = 0
		uncov_bases = 0

		barcode_name = file.split('-')[0]
		sample_name = dictionary[barcode_name]
		ref_name = file.split('REF_')[1].split(':')[0]
		command = (f"samtools depth -a {file}")
		output = Popen(['bash', '-c', command], stdout=PIPE)
			
		for line in output.stdout:
			try:

				overall += 1
				line = line.decode('utf8')
				coverage = line.split('\t')[2]
			
				if int(coverage) >= 10:
					cov_10 += 1
				if int(coverage) == 0:
					uncov_bases += 1	
					
			except:
				continue		 
		if overall > 0:		
			C10 = cov_10 / overall
			C10 = round(C10, 2)
		else:
			C10 = 0.0

		if cov_10 > 0:		
			print(f'{sample_name}\t{ref_name}\t{C10}\t{uncov_bases}')  

def main():
	infiles = args.infiles
	name_dictionary = make_name_dictionary()
	run_samtools(infiles, name_dictionary)


if __name__ == "__main__":
	main()