#!/usr/bin/env python3

# query_mongo_return_fastqs.py

# This is a helper script for the kraken-bracken workflow running kraken-bracken individually from a list of RSP files.

import argparse
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
import re 

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input BLAST output file, to be filtered by best hit per contig')
	parser.add_argument('-a', '--accession', help = 'RSP to query', required = True, dest = 'accession')
	args = parser.parse_args()
	accession = args.accession
	return accession

def connect_to_mongo():
#	dotenv_path = Path('/Users/liamkane/tokens/kannapedia_mongo_credentials')
#	load_dotenv(dotenv_path=dotenv_path)

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']
	return collection 


def query_mongo(rsp, collect):

	for i in collect.find({"_id":rsp}):
		print(i['fastq_link'][0])
		print(i['fastq_link'][1])

def main():
	infile = parse_arguments()
	collection = connect_to_mongo()
	query_mongo(infile, collection)

if __name__ == '__main__':
	main()