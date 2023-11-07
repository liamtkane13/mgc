#!/usr/bin/eny python3

# compare_variants_of_interest.py

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

