#!/usr/bin/env python3

# print_out_male_RSPs.py

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


    regx = re.compile('RSP[0-9]')
    srr_regx = re.compile('SRR[0-9]')

    for i in collection.find({"_id":regex}):
    	if i['plant_sex'] == 'Male':
    		print(i['_id'])


def main():
	query_mongo()


if __name__ == '__main__':
	main()	    		 