#!/usr/bin/env python3

# add_columns_to_HVV_csv.py

# this is going to be a one off script, so there may be some hardcoding

import argparse
import pandas as pd
from pymongo import MongoClient
import os 
import re

def parse_arguments():
	parser = argparse.ArgumentParser(description='Path to the HVV CSV to edit')
	parser.add_argument('-i', '--infile', help = 'Happy Valley CSV', required = True, dest = 'infile')
	args = parser.parse_args()
	infile = args.infile
	return infile


def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
		username = 'kannapedia',
		password = os.environ['KANNAPEDIA_PWORD'],
		authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']

	return collection

def query_mongo_and_alter_csv(file, collect):

	df = pd.read_csv(file)
	print(df)

	list_of_lists = []

	for rsp in df['RSP']:

		for i in collect.find({'_id':rsp}):

			baby_list = []

			acc = i['_id']
			y_ratio = i['y_ratio']['y_to_all_ratio']
			dist_to_11641 = i['ALL_distance']['RSP11641-Super_Lemon_Haze']


			if i['_id'] == 'RSP13067':

				dist_to_13067 = '0.00'
				dist_to_13066 = i['ALL_distance']['RSP13066-Super_Lemon_Haze']

			elif i['_id'] == 'RSP13066':

				dist_to_13067 = i['ALL_distance']['RSP13067-Super_Lemon_Haze']
				dist_to_13066 = '0.00'
			else:	

				dist_to_13066 = i['ALL_distance']['RSP13066-Super_Lemon_Haze']
				dist_to_13067 = i['ALL_distance']['RSP13067-Super_Lemon_Haze']

			baby_list = [acc, y_ratio, dist_to_13067, dist_to_13066, dist_to_11641]	
			list_of_lists.append(baby_list)


	new_df = pd.DataFrame(list_of_lists, columns = ['RSP', 'Y ratio', 'Distance to RSP13067', 'Distance to RSP13066', 'Distance to RSP11641'])
	print(new_df)
	complete_df = pd.merge(df, new_df, on = ['RSP'])
	print(complete_df)

	complete_df.to_csv('HappyValley_heterozygosity_y-ratio_genetic_distances.tsv', sep='\t', header=True, index=False)	

def main():
	
	infile = parse_arguments()
	collection = connect_to_mongo()
	query_mongo_and_alter_csv(infile, collection)

if __name__ == '__main__':
	main()		