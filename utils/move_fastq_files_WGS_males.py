#!/usr/bin/env python3

# move_fastq_files_WGS_males.py

from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os 
from subprocess import check_output as do 

def query_mongo():
	dotenv_path = Path('/Users/liamkane/tokens/kannapedia_mongo_credentials')
	load_dotenv(dotenv_path=dotenv_path)

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']
	with open('/Users/liamkane/software/liam_git/utils/samples_to_remap.txt', 'r') as file:
		for line in file: 
			rsp = line.strip('\n')
			data = collection.find({"_id":rsp})
			for i in data:
				link_end_0 = (i['fastq_link'][0]).split('com')[1]
				link_end_1 = (i['fastq_link'][1]).split('com')[1]
				command_1 = (f'aws s3 cp s3://mgcdata{link_end_0} s3://mgcdata/SS2/bams-JL_Y/fastq_remap/')
				command_2 = (f'aws s3 cp s3://mgcdata{link_end_1} s3://mgcdata/SS2/bams-JL_Y/fastq_remap/')
				do(['bash', '-c', command_1])
				do(['bash', '-c', command_2])
				print(f'Moved {rsp} FASTQs')


def main():
	query_mongo()

if __name__ == '__main__':
	main()	