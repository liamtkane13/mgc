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


def query_from_40Genome_files():
    naming_dict = {}
    with open('/Users/liamkane/software/liam_git/utils/Sample_info.txt', 'r') as file:
        with open('/Users/liamkane/software/liam_git/utils/rsp-to-sample.txt', 'r') as file2:
            for lines in file2:
                rsp = lines.split('\t')[0]
                sample_n = lines.split('\t')[1].rstrip('\n')
                naming_dict[sample_n] = rsp
                for line in file:
                    sample_name = line.split('\t')[0]
                    sex = line.split('\t')[4]
                    print(naming_dict)
                    if sample_name in naming_dict:
                        processed_rsp = naming_dict[sample_name]
                        print(processed_rsp)



def main():
#    query_mongo()
    query_from_40Genome_files()


if __name__ == '__main__':
	main()	    		 