#!/usr/bin/env python3

# query_mongo_return_fastqs.py

# This is a helper script for the kraken-bracken workflow running kraken-bracken individually from a list of RSP files.

import argparse
from pymongo import MongoClient
import os
import re 

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input BLAST output file, to be filtered by best hit per contig')
	parser.add_argument('-a', '--accession', help = 'RSP to query', required = True, dest = 'accession')
	args = parser.parse_args()
	accession = args.accession
	return accession

def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']
	return collection 


def query_mongo(rsp, collect):

	for i in collect.find({"_id":rsp}):
		link_1 = i['fastq_link'][0] 
		link_2 = i['fastq_link'][1]
		processed_link_1 = link_1.lstrip('https://mgcdata.s3.amazonaws.com')
		processed_link_2 = link_2.lstrip('https://mgcdata.s3.amazonaws.com')
		final_link_1 = ('s3://mgcdata/' + processed_link_1)
		final_link_2 = ('s3://mgcdata/' + processed_link_2)
		print(final_link_1)
		print(final_link_2)

def main():
	infile = parse_arguments()
	collection = connect_to_mongo()
	query_mongo(infile, collection)

if __name__ == '__main__':
	main()