#!/usr/bin/env python3

# query_mongo_Males_Mapped.py

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

    with open('/Users/liamkane/software/liam_git/utils/rsps_for_samtools.txt', 'r') as file:
        for line in file:
            rsp = line.strip('\n')
            data = collection.find({"_id":rsp})
            for i in data:
#                print(f"{rsp}:\t{i['bam_file_url']}")
                print(i['bam_file_url'])


def main():
    query_mongo()

if __name__ == '__main__':
    main()