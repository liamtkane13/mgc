#!/usr/bin/eny python3

# compare_variants_of_interest.py 

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


	for i in collect.find({'_id':rsp1}):

		rsp1_var = i['kannapedia_variants']

	for i in collect.find({'_id':rsp2}):

		rsp2_var = i['kannapedia_variants']	

	rsp1_df = pd.DataFrame.from_dict(rsp1_var)
	rsp2_df = pd.DataFrame.from_dict(rsp2_var)

#	print(rsp1_df)
#	print(rsp2_df)

	rsp1_only_var = (rsp1_df[~rsp1_df.HGVSc.isin(rsp2_df.HGVSc)])
	rsp2_only_var = (rsp2_df[~rsp2_df.HGVSc.isin(rsp1_df.HGVSc)])
	overlap_df = (rsp1_df[rsp1_df.HGVSc.isin(rsp2_df.HGVSc)])
	
#	print(rsp1_only_var)
#	print(rsp2_only_var)
#	print(overlap_df)
	rsp1_only_var_len = len(rsp1_only_var)
	rsp2_only_var_len = len(rsp2_only_var)
	overlapped_var_len = len(overlap_df)


	file1 = (f'variants_unique_to_{rsp1}_vs_{rsp2}.tsv')
	file2 = (f'variants_unique_to_{rsp2}_vs_{rsp1}.tsv')
	overlap_file = (f'{rsp1}_{rsp2}_shared_variants.tsv')

	rsp1_df.to_csv(file1, sep='\t')
	rsp2_df.to_csv(file2, sep='\t')	
	overlap_df.to_csv(overlap_file, sep='\t')
	print(f'{rsp1}_only_variants: {rsp1_only_var_len}')
	print(f'{rsp2}_only_variants: {rsp2_only_var_len}')
	print(f'Shared_variants: {overlapped_var_len}')




def main():
	
	rsp_1, rsp_2 = parse_arguments()
	collection = connect_to_mongo()	
	compare_variants(rsp_1, rsp_2, collection)

if __name__ == '__main__':
	main()	