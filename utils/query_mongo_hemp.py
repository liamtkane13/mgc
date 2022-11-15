#!/usr/bin/env python3

# query_mongo_hemp.py

from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os 
import re


def query_mongo():
	dotenv_path = Path('/Users/liamkane/tokens/kannapedia_mongo_credentials')
	load_dotenv(dotenv_path=dotenv_path)

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']


	regex = re.compile('RSP[0-9]')
	srr_regex = re.compile('SRR[0-9]')

	for i in collection.find({"_id":regex}):
		if i['strain_type'] == 'Type III':
			print(f"{i['_id']}\t{i['strain_type']}")
		if i['strain_type'] == 'Type IV':
			print(f"{i['_id']}\t{i['strain_type']}")

	for it in collection.find({"_id":srr_regex}):
		if it['strain_type'] == 'Type III':
			print(f"{it['_id']}\t{it['strain_type']}")
		if it['strain_type'] == 'Type IV':
			print(f"{it['_id']}\t{it['strain_type']}")

def main():
	query_mongo()

if __name__ == '__main__':
	main()				