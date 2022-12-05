#!/usr/bin/env python3

# find_incorrect_psp_fastqs.py

def iterate_through_tsv():
	with open('/Users/liamkane/Desktop/Bioinformatics/psp_to_raw_files.tsv','r') as file:
		for line in file:
			psp = str(line.split('\t')[0])
			direction = str(line.split('\t')[1])
			fastq = str(line.split('\t')[2].rstrip('\n'))
			if direction not in fastq:
				print(f'{psp} {direction} is a duplicate')


def main():
	iterate_through_tsv()

if __name__ == '__main__':
	main()