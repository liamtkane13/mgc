#!/usr/bin/env python3

# print_bam_url_from_RSP_list.py

import argparse
from pymongo import MongoClient
import os
import re


def parse_arguments():
	parser = argparse.ArgumentParser(description='Input a list of RSPs to find BAM files for')
	parser.add_argument('-i', '--infile', help = 'List of RSPs to find BAMs for', required = True, dest = 'infile')
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


def print_s3_bam_paths(file, collect):

	with open(file, 'r') as file:

		for rsp in file:

			rsp = rsp.rstrip('\n')

			for i in collect.find({'_id':rsp}):

				bam_url = i['bam_file_url']

				back_of_url = bam_url.split('.com/')[1]

				s3_form = 's3://mgcdata/' + back_of_url
				
				print(f'{rsp}\t{s3_form}')


def main():
	
	infile = parse_arguments()
	collection = connect_to_mongo()
	print_s3_bam_paths(infile, collection)		

if __name__ == '__main__':
	main()			