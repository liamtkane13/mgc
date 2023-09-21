#!/usr/bin/env python3

# print_variants_from_mongo.py

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

def print_variants(rsp, collect):

	number = re.compile('[0-9]')

	for i in collect.find({'_id': rsp}):

		print(i['kannapedia_variants'])

def main():
	accession = parse_arguments()
	collection = connect_to_mongo()
	print_variants(accession, collection)

if __name__ == '__main__':
	main()			