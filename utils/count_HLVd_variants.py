#!/usr/bin/env python3

# count_HLVd_variants.py

import json

def count_variants():

	all_variants = json.loads((open('/Users/liamkane/Desktop/variants-HLVd-05-05-2023.json', 'r').read()))


#	total_counter = 0
	print(f"variant\tcounts\tpercentage")

	for i in all_variants:

		if all_variants[i]['distinct_submitters'] == ['Phylos Oregon (10-APR-2019)']: 
			continue

		elif all_variants[i]['distinct_submitters'] == ['Phylos CA (10-APR-2019)']:
			continue

		elif all_variants[i]['distinct_submitters'] == ['Phylos CA (10-APR-2019)', 'Phylos Oregon (10-APR-2019)']:
			continue

		else:
			count = int(len(all_variants[i]['accession_list']))
			percent = round(((float(count / int(243))) * 100), 2)
			
			if count >= 3:
				print(f"{i}\t{len(all_variants[i]['accession_list'])}\t{percent}%")

#	samples = json.loads((open('/Users/liamkane/software/mgc_qc/mongo_django/mysite/viropedia/json/HLVd-all-gbk-05-05-2023.json', 'r').read()))

#	for i in samples:
#		try:
#			if 'Phylos' in samples[i]["submitter_nick"]:
#				continue				
#			else:	
#				print(f'{i}\t{samples[i]["variants"]}')
#		except:
#			print(f'{i}\t{samples[i]["variants"]}')		
		

def main():
	count_variants()

if __name__ == '__main__':
	main()	 