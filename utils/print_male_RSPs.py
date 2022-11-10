#!/usr/bin/env python3

# print_male_RSPs.py

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

        try:
            sex = i['plant_sex']
            if sex == 'Male':
                if i['ss_version'] == 'WGS':
                    print(i['_id'])

        except:
            continue        


def main():
	query_mongo()


if __name__ == '__main__':
	main()	    		 