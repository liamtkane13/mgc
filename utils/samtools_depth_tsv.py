#!/usr/bin/env python3

import argparse
from glob import glob 
from subprocess import check_output as run

parser = argparse.ArgumentParser(description='Input BAM files for samtools depth, to be output as a tsv file')
parser.add_argument('-i', '--infiles', nargs = '+', help = 'BAM files for samtools', required = True, dest = 'infiles')
args = parser.parse_args()



def run_samtools(files):
	for file in files:
		sample_name = file.split('-')[0]
		ref_name = file.split('REF_')[1].split(':')[0]
		print(f"{sample_name}\t{file}")
		command = (f"samtools depth -a {file}")
		output = run(['bash', '-c', command])
		for line in output:
			line = line.decode('utf8')
			print(line)
		print(output)	
#			print(f'{sample_name}\t{ref_name}\t{line}')
#		split_output = output.split('\n')
#		print(split_output)

def main():
	infiles = args.infiles
	run_samtools(infiles)


if __name__ == "__main__":
	main()