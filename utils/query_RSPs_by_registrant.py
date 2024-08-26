import argparse
from pymongo import MongoClient
import os
import re 

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input a Registrant name to query')
	parser.add_argument('-r', '--registrant', help = 'Registrant to query', required = True, dest = 'registrant')
	args = parser.parse_args()
	registrant = args.registrant
	return registrant

def connect_to_mongo():

	mongo = MongoClient(os.environ['MONGO_HOST'],
			username = 'kannapedia',
			password = os.environ['KANNAPEDIA_PWORD'],
			authSource = 'mgc_ss2_JL')

	database = mongo['mgc_ss2_JL']
	collection = database['SS2']
	return collection 

def query_mongo(collect, reg):

	rsp = re.compile('RSP[0-9]')

	for i in collect.find({'_id': rsp}):

		if i['registrant'] == reg:
			
			print(i['_id'])

def main():
	
	registrant = parse_arguments()
	collection = connect_to_mongo()
	query_mongo(collection, registrant)

if __name__ == '__main__':
	main()			