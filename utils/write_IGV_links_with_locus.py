#!/usr/bin/env python3

# write_IGV_links.py

# This is a helper script for the make_IGV_links.nf workflow

import argparse
from subprocess import check_output as run 

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the corresponding s3 path for IGV Link creation')
    parser.add_argument('-b', '--bucket', help = 's3 bucket for analysis', required = True, dest = 'bucket')
    parser.add_argument('-l', '--locus', help = 'Locus for use in IGV Link', required = True, dest = 'locus')
    args = parser.parse_args()
    bucket = args.bucket
    locus = args.locus
    return bucket, locus

def produce_links(buck, lo):
	
	ls_command = (f'aws s3 ls s3://mgcdata/shared/igv-links/tmp/{buck}/')
	ls_output = (run(['bash', '-c', ls_command])).decode('utf8').rstrip('\n')
	raw_output = ls_output.split(' ')

	bam_files = []
	counter = 0

	for i in raw_output:
		if 'bam' in i:
			if 'bai' in i:
				continue
			else:    
				bam = i.split('\n')[0]
			bam_files.append(bam)
		if 'fasta' in i:
			if 'fai' in i:
				continue
			else:	
				ref = i.split('\n')[0]    

	igv_link = "http://localhost:60151/load?file=" 

	for file in bam_files:
		counter += 1
		if counter == 1:
			file_link = (f'https://mgcdata.s3.amazonaws.com/shared/igv-links/tmp/{buck}/{file}')
		else:
			file_link = (f',https://mgcdata.s3.amazonaws.com/shared/igv-links/tmp/{buck}/{file}')
		igv_link = igv_link + file_link
	end_of_link = (f"&genome=https://mgcdata.s3.amazonaws.com/shared/igv-links/tmp/{buck}/{ref}&locus={lo}")
	final_igv_link = igv_link + end_of_link

	with open('igv_link.txt', 'w') as outfile:
		outfile.write(final_igv_link)
	outfile.close()	



def main():
	bucket, locus = parse_arguments()
	produce_links(bucket, locus)

if __name__ == '__main__':
	main()	
     