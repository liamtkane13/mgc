#!/usr/bin/env python3

# make_virus_dict.py

# silly script!

def make_virus_dict():

	virus_dict = {}

	with open('/Users/liamkane/Desktop/out/full_virus_names.txt', 'r') as file:
		for line in file:
			line = line.strip('\n')
			accession = line.split('|')[3]
#			print(accession)
			virus_dict[accession] = line

	print(virus_dict)		


def main():
	make_virus_dict()


if __name__ == '__main__':
	main()