#!/usr/bin/env python3

# print_sex_and_s3_bam_paths.py

from pymongo import MongoClient
from pathlib import Path
import os 
import re

def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']

	return collection

def print_output_tsv(collect):

	regex = re.compile('RSP[0-9]')

	counter = 0

	for i in collect.find({"_id":regex}):

		try:
			rsp = i['_id']
			mongo_sex = i['plant_sex']
			mongo_ver = i['ss_version']	
			bam_link = i['bam_file_url']
			ref_length = str(i['align_metrics_detail']['Bases_in_reference_genome'])
			pub = str(i['published'])
#			print(f'{rsp}\t{ref_length}')

		except:
			continue


#		if ref_length == '951600078' and mongo_ver == 'WGS':
#			print(f'{rsp}\t{mongo_sex}\t{bam_link}')	
		if ref_length == '876754411' and mongo_sex == 'Female' and mongo_ver == 'WGS':# and pub == 'false':
			counter += 1
			print(rsp)
	print(f'Number of female samples mapped to JL_female: {counter}')				

def main():
	
	collection = connect_to_mongo()
	print_output_tsv(collection)

if __name__ == '__main__':
	main()			