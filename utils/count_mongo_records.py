#!/usr/bin/env python3

# count_mongo_records.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path

def connect_to_mongo():
    dotenv_path = Path('/Users/liamkane/tokens/kannapedia_mongo_credentials')
    load_dotenv(dotenv_path = dotenv_path)
    mongo = MongoClient(os.environ['MONGO_HOST'],
            username = 'liam',
            password = os.environ['MGC_QC_PWORD'],
            authSource = 'mgc_ss2_JL')
    db = mongo['mgc_ss2_JL']
    collection = db['mgc_qc']

    return collection


def count_records(collect):

	for i in collect.find():

		counter = 0
		
		for key in i:
			counter +=1

		if counter < 33:

			print(f"{i['_id']}\t{counter}")	
			

def main():
	collection = connect_to_mongo()
	count_records(collection)

if __name__ == '__main__':
	main()	