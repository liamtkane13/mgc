#!/usr/bin/eny python3

# print_RSPs_by_sex_and_seq_type.py

from pymongo import MongoClient
from pathlib import Path
import os 
import re
import argparse

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input BLAST output file, to be filtered by best hit per contig')
	parser.add_argument('-s', '--sex', help = 'Plant sex to query', required = True, dest = 'sex')
	parser.add_argument('-t', '--type', help = 'Sequencing type to query', required = True, dest = 'type')
	args = parser.parse_args()
	sex = args.sex
	seq_type = args.type
	return sex, seq_type


def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']

	return collection


def query_mongo(seks, seq, collect):

	regex = re.compile('RSP[0-9]')

	for i in collect.find({"_id":regex}):

		try:
			mongo_sex = i['plant_sex']
			mongo_ver = i['ss_version']
			if mongo_sex == seks and mongo_ver == seq:
				print(i['_id'])

		except:
			continue

def main():

	sex, seq_type = parse_arguments()
	collection = connect_to_mongo()
	query_mongo(sex, seq_type, collection)

if __name__ == '__main__':
	main()	