#!/usr/bin/env python3

# parse_genes_of_interest_for_missense_mutations.py

import argparse
import csv
from subprocess import check_output as run
from pymongo import MongoClient
import os
import re  

def parse_arguments():

	parser = argparse.ArgumentParser(description='Input a list of genes and a VCF file to parse')
	parser.add_argument('-i', '--infile', help = 'List of genes', required = True, dest = 'infile')
	args = parser.parse_args()
	infile = args.infile
	return infile


def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']
	return collection 	

def parse_variants(tsv):
	
	list_of_genes = []

	with open(tsv) as tsv:
		tsv_file = csv.reader(tsv, delimiter = '\t')
		for row in tsv_file:
			gene_name = row[3]
			list_of_genes.append(gene_name)
			mRNA_id = row[5]
			coordinates = (f'{row[0]}:{row[1]}-{row[2]}')
#			print(mRNA_id)
#			print(coordinates)
#			tabix_command = (f'tabix -p {coordinates} {vcf}')
#			tabix_output = run(['bash', '-c', tabix_command])
#			print(f'{mRNA_id}\n{tabix_output}\n')
	return list_of_genes

def print_out_high_impact_variants(collect, list_ob):

	regex = re.compile('RSP[0-9]')

	queried_name_list = []
	queried_name_hash = {}

	for i in collect.find({'_id':regex}):

		try:
			for it in i['variants']:
				if it['Annotation_Impact'] == 'LOW':
					continue
				else:	
#					print(f"{it['HGVSp']}\t{it['region_label']}")
					queried_name = it['region_label']
					#queried_info = f'{it["gene_name"]}\t{it["HGVSp"]}'

					if queried_name not in queried_name_list:
						queried_name_list.append(queried_name)
					
#					elif queried_name not in queried_name_hash:
#							queried_name_hash[queried_name] = queried_info 
#					if queried_name in list_ob:
#						print(queried_name)
		except:
			continue	



#	print(list_ob)
	print(queried_name_list)
#	print(set(queried_name_list).intersection(list_ob))	
	print(len(set(queried_name_list).intersection(list_ob)))
	print(queried_name_hash)



def main():
	
	collection = connect_to_mongo()
	infile = parse_arguments()
	list_of_genes = parse_variants(infile)
	print_out_high_impact_variants(collection, list_of_genes)

if __name__ == '__main__':
	main()					