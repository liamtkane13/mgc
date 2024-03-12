#!/usr/bin/env python3

# calculate_y_ratio_from_idxstats_output.py

# This script mimics the function of the strainseek script `samtools_idxstats_y_ratio.pl`, 
# and calculates the Y ratio from a TSV output of samtools idxstats.

import argparse


def parse_arguments():
	parser = argparse.ArgumentParser(description='Input samtools idxstats output in TSV format for analysis')
	parser.add_argument('-i', '--infiles', help = 'TSV to crunch', nargs = '+', required = True, dest = 'infiles')
	args = parser.parse_args()
	infiles = args.infiles
	return infiles

	

def parse_tsv_no_pandas(files):

	print(f"RSP\tTotal Mapped\tTotal Y Mapped\tY Ratio")

	for file in files:

		if '/' in file:

			rsp = file.split('/')[-1].split('.')[0].split('-')[0]

		else:	

			rsp = file.split('.')[0].split('-')[0]
	
		with open(file, 'r') as file:

			total_mapped = 0
			total_y_mapped = 0

			for line in file:

				(chr_name, chr_length, mapped, unmapped) = line.split('\t')

				mapped = int(mapped)
				chr_name = str(chr_name)

				total_mapped += mapped

				if 'arrow' in chr_name:

					total_y_mapped += mapped

				y_ratio = float(total_y_mapped/total_mapped)

		print(f"{rsp}\t{total_mapped}\t{total_y_mapped}\t{y_ratio}")		

	

def main():

	infiles = parse_arguments()
	parse_tsv_no_pandas(infiles)

if __name__ == '__main__':
	main()	 