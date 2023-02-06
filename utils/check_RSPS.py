#!/usr/bin/env python3

from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv
import os


dotenv_path = Path('/Users/liamkane/tokens/kannapedia_mongo_credentials')
load_dotenv(dotenv_path = dotenv_path)

mongo = MongoClient(os.environ['MONGO_HOST'],
        username = 'kannapedia',
        password = os.environ['KANNAPEDIA_PWORD'],
        authSource = 'mgc_ss2_JL')

db = mongo['mgc_ss2_JL']
collection = db['SS2']

def check_RSPs_mongo():
	with open('/Users/liamkane/Desktop/Bioinformatics/media-3_RSP.csv', 'r') as file:
		for line in file:
			rsp = line.split(',')[1]
#			print(rsp)
			for i in collection.find({"_id":rsp}):
#				print(f"ID is {i['_id']}")	
				status = i['hide_from_tree']
#					status = i['hide_from_tree']
				if status == 'true':
						print(f"{rsp} is private")

def main():
	check_RSPs_mongo()


if __name__ == '__main__':
	main()				