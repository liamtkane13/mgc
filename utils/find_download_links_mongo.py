#!/usr/bin/env python3

from pymongo import MongoClient
import os
import re 

def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']

	return database

def query_mongo(db):

	ont = db['ONT']
	psp = db['PSP']
	ss1 = db['SS1']
	ss2 = db['SS2']

		

def main():
	
	database = connect_to_mongo()
	query_mongo(database)

if __name__ == '__main__':
	main()			