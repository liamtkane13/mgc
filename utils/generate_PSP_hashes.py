#!/usr/bin/env python3

# generate_PSP_hashes.py

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


def generate_hashes(collect):
	with open('/Users/liamkane/software/psp-tmp/psp-needing-hashes.txt', 'r') as file:
		for line in file:
			psp = line.strip('\n')
			print(psp)
			database = collect.find({'_id':psp})
			for i in database:
				link_end_1 = (i['fastq_link'][0]).split('com')[1]
				link_end_2 = (i['fastq_link'][1]).split('com')[1]
				print(f's3://mgcdata{link_end_1}')
				print(f's3://mgcdata{link_end_2}')

def main():
	collection = connect_to_mongo()
	generate_hashes(collection)


if __name__ == '__main__':
	main()	