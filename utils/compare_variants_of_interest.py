#!/usr/bin/eny python3

# compare_variants_of_interest.py

# This script was written to compare variants of RSP 1 with its lower coverage counterpart, RSP 2. As such, this script only checks which variants are in RSP 1, but not RSP 2. Update this for more use cases. 

import argparse
from pymongo import MongoClient
import os
import re 
import pandas as pd 

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



def compare_variants(rsp1, rsp2, collect):

	rsp1_list = []
	rsp2_list = []

	for i in collect.find({'_id':rsp1}):

		rsp1_var = i['kannapedia_variants']
		
		for it in rsp1_var:
			var = it['HGVSc']
			rsp1_list.append(var)	

	for i in collect.find({'_id':rsp2}):

		rsp2_var = i['kannapedia_variants']
		
		for it in rsp2_var:
			var = it['HGVSc']
			rsp2_list.append(var)		

	rsp1_df = pd.DataFrame.from_dict(rsp1_var)
	rsp2_df = pd.DataFrame.from_dict(rsp2_var)
	print(rsp1_df)
	print(rsp2_df)
#	print(rsp1_list)
#	print(rsp2_list)

	rsp1_only_var = (rsp1_df[~rsp1_df.HGVSc.isin(rsp2_df.HGVSc)])
	rsp2_only_var = (rsp2_df[~rsp2_df.HGVSc.isin(rsp1_df.HGVSc)])
	print(rsp1_only_var)
	print(rsp2_only_var)


def main():
	
	rsp_1, rsp_2 = parse_arguments()
	collection = connect_to_mongo()	
	compare_variants(rsp_1, rsp_2, collection)

if __name__ == '__main__':
	main()	