#!/usr/bin/env python3

# delete_old_mongo_backup.py

from datetime import datetime
from subprocess import check_output as run

def do_the_thing():

	date_list = []

	ls_command = (f"aws s3 ls s3://mgcdata/backup/mongodb/bson/ | cut -f 2 -d 'E' | cut -f 2 -d ' ' | cut -f 1 -d '/'")
	ls_output = ((run(['bash', '-c', ls_command])).decode('utf8')).rstrip('\n')
	dates = ls_output.split('\n')
	for i in dates:
		it = datetime.strptime(i, "%Y%m%d")
		date_list.append(it)
	oldest = ((str(min(date_list))).split(' ')[0]).replace('-', '')
	rm_command = (f'aws s3 rm s3://mgcdata/backup/mongodb/bson/{oldest}/ --recursive')	
	run(['bash', '-c', rm_command])


def main():
	do_the_thing()

if __name__ == '__main__':
	main()	