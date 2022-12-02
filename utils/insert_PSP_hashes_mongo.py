#!/usr/bin/env python3

# insert_PSP_hashes_mongo.py

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

def insert_hashes(collect):
	with open('/Users/liamkane/software/liam_git/utils/PSP_hashes.txt', 'r') as file:
		for line in file:
			
			sha_hash = line.split('  ')[0]
			fastq = line.split('  ')[1]
			psp = fastq.split('_')[0]
			print(psp)
			data_json = collect.find({'_id':psp})
			for i in data_json:
				print(i['fastq_link'][0])


def main():
	collection = connect_to_mongo()
	insert_hashes(collection)			 		

if __name__ == "__main__":
	main()	