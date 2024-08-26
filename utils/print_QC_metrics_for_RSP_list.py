#!/usr/bin/env python3

# print_QC_metrics_for_RSP_list.py

from pymongo import MongoClient
import os 
import re
import argparse

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input list of RSPs to query')
	parser.add_argument('-i', '--infile', help = 'List of RSPs to query', required = True, dest = 'infile')
	args = parser.parse_args()
	infile = args.infile
	return infile

def connect_to_mongo():
	
	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['mgc_qc']

	return collection

def query_QC_metrics(file, collect):

	print(f'RSP\tPlant_Sex\tMean_Cov\tMedian_Cov\tInsert_Size\tPercent_Aligned')

	with open(file, 'r') as file:

		for rsp in file:
			rsp = rsp.rstrip('\n')

			for i in collect.find({'_id': rsp}):

				avg_cov = i['report_general_stats_data'][0][rsp]['mean_coverage']
				median_cov = i['report_general_stats_data'][0][rsp]['median_coverage']
				insert_size = i['report_general_stats_data'][0][rsp]['median_insert_size']
				mapping_percent_raw = i['report_general_stats_data'][0][rsp]['percentage_aligned']
				mapping_percent = str(round(mapping_percent_raw, 2))

				try:

					plant_sex = i['plant_sex']

				except:
					plant_sex = 'Check Manually'	
			
				print(f'{rsp}\t{plant_sex}\t{avg_cov}\t{median_cov}\t{insert_size}\t{mapping_percent}')
				

def main():

	infile = parse_arguments()
	collection = connect_to_mongo()
	query_QC_metrics(infile, collection)

if __name__ == '__main__':
	main()	