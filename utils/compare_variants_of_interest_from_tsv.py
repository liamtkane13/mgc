#!/usr/bin/env python3

# compare_variants_of_interest_from_tsv.py

import argparse
from pymongo import MongoClient
import os
import re 
import pandas as pd 

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input a TSV file with RSPs to query')
	parser.add_argument('-t', '--tsv', help = 'TSV with RSPs to query', required = True, dest = 'tsv')
	args = parser.parse_args()
	tsv = args.tsv
	return tsv

def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']
	return collection 

def append_row(df, row):
    return pd.concat([
                df, 
                pd.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)	

def compare_variants(file, collect):

	data_list = []

	with open(file) as file:
		
		for line in file:
			rsp1 = line.split('\t')[0]
			rsp2 = line.split('\t')[1].rstrip('\n')

#			data_list = []

			for i in collect.find({'_id':rsp1}):

				rsp1_var = i['kannapedia_variants']

			for i in collect.find({'_id':rsp2}):

				rsp2_var = i['kannapedia_variants']	

			rsp1_df = pd.DataFrame.from_dict(rsp1_var)
			rsp2_df = pd.DataFrame.from_dict(rsp2_var)	

			rsp1_only_var = (rsp1_df[~rsp1_df.HGVSc.isin(rsp2_df.HGVSc)])
			rsp2_only_var = (rsp2_df[~rsp2_df.HGVSc.isin(rsp1_df.HGVSc)])
			overlap_df = (rsp1_df[rsp1_df.HGVSc.isin(rsp2_df.HGVSc)])
				
			rsp1_only_var_len = len(rsp1_only_var)
			rsp2_only_var_len = len(rsp2_only_var)
			overlapped_var_len = len(overlap_df)	

			rsp_id = (f'{rsp1} and {rsp2}')

			data_list.append([rsp_id, rsp1_only_var_len, rsp2_only_var_len, overlapped_var_len])
	

	output_df = pd.DataFrame(data_list, columns=['RSPs', 'RSP1_unique_variants', 'RSP2_unique_variants', 'Shared_variants']) 
	
	print(output_df)	

	output_df.to_csv('rsp_variant_comparison.tsv', sep='\t')		


def main():
	tsv = parse_arguments()
	collection = connect_to_mongo()
	compare_variants(tsv, collection)

if __name__ == '__main__':
	main()