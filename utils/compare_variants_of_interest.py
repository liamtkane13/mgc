#!/usr/bin/eny python3

# compare_variants_of_interest.py

import argparse
from pymongo import MongoClient
import os
import re 

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input BLAST output file, to be filtered by best hit per contig')
	parser.add_argument('-r1', '--rsp_1', help = 'RSP 1 to query', required = True, dest = 'rsp_1')
	parser.add_argument('-r2', '--rsp_2', help = 'RSP 2 to query', required = True, dest = 'rsp_2')
	args = parser.parse_args()
	rsp_1 = args.rsp_1
	rsp_2 = args.rsp_2
	return rsp_1, rsp_2

def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']
	return collection 

def compare_variants(rsp1, rsp2):