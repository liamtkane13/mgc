#!/usr/bin/env python3 

# compare_psilocybe_sha256.py

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
	collection = database['PSP']

	return collection 	


def sha256sum_fastqs_and_check_mongo(collect):
	regex = re.compile('PSP[0-9]')
#	with open('/Users/liamkane/Desktop/Bioinformatics/psilocybe_samples.txt', 'r') as file:
#		for line in file:
	for i in collect.find({"_id":regex}):
		try:
			print(i['fastq_hash']['original']['fq1']['sha256sum'])
		except:
			continue



def main():
	collection = connect_to_mongo()
	sha256sum_fastqs_and_check_mongo(collection)


if __name__ == '__main__':
	main()		