#!/usr/bin/env python3

# print_ss_v3_samples.py

from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os 
import re

def connect_to_mongo():
	dotenv_path = Path('/Users/liamkane/tokens/kannapedia_mongo_credentials')
	load_dotenv(dotenv_path=dotenv_path)

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']

	return collection

def print_ss_v3(coll):

	regx = re.compile('RSP[0-9]')
	for i in coll.find({"_id":regx}):
		if i['ss_version'] == 'V3':
			print(i['_id'])

def main():
	collection = connect_to_mongo()
	print_ss_v3(collection)

if __name__ == '__main__':
	main()	    			