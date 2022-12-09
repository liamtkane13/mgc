#!/usr/bin/env python3

# get_male_WGS_coverage.py

from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os 
import re
from subprocess import check_output as run

def connect_to_mongo():
	dotenv_path = Path('/Users/liamkane/tokens/kannapedia_mongo_credentials')
	load_dotenv(dotenv_path=dotenv_path)

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['mgc_qc']

	return collection


def query_male_coverage(collect):
	with open('/Users/liamkane/Desktop/Bioinformatics/male_sample_list.txt', 'r') as file:
		for sample_name in file:
			sample_name = sample_name.rstrip('\n')
			
			try:
				for i in collect.find({"_id":sample_name}):
					print(f"{sample_name}\t{i['report_general_stats_data'][0][sample_name]['mean_coverage']}")	

			except:
				print(f"{sample_name} not in MongoDB")		


def main():
	collection = connect_to_mongo()	
	query_male_coverage(collection)

if __name__ == '__main__':
	main()	