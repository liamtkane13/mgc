#!/usr/bin/env python3

# print_WGS_males_from_mongo.py

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

def query_mongo_return_males(collect):

	regex = re.compile('RSP[0-9]')

	for i in collect.find({'_id': regex}):

		try:
			sex = i['plant_sex']
			if sex == 'Male':
				if i['ss_version'] == 'WGS':
					print(i['bam_file_url'])
		except:
			continue				

def main():

	collection = connect_to_mongo()
	query_mongo_return_males(collection)

if __name__ == '__main__':
	main()	                