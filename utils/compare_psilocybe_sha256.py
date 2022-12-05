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
	with open('/Users/liamkane/Desktop/Bioinformatics/psilocybe_samples.txt', 'r') as file:
		for line in file:
			bucket = line.split('\t')[0]
			sample = line.split('\t')[1].strip('\n')

			download_command = (f'aws s3 cp s3://mgcdata/SS2/runs/{bucket}{sample} .')
			sha_command = (f'sha256sum {sample}')
			delete_sample = (f'rm {sample}')
			run(['bash', '-c', download_command])
			sha256sum = ((run(['bash', '-c', sha_command])).decode('utf8')).split('  ')[0]
			run(['bash', '-c', delete_sample])




			for i in collect.find({"_id":regex}):
				if sha256sum == (i['fastq_hash']['original']['fq1']['sha256sum']):
					print(f"{i['_id']} R1 is {sample}")
				if sha256sum == (i['fastq_hash']['original']['fq2']['sha256sum']):	
					print(f"{i['_id']} R2 is {sample}")



def main():
	collection = connect_to_mongo()
	sha256sum_fastqs_and_check_mongo(collection)


if __name__ == '__main__':
	main()		