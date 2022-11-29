#!/usr/bin/env python3

# find_illumina_samples_wo_RSPs.py

from subprocess import check_output as run

def query_s3():
	with open('/Users/liamkane/Desktop/Bioinformatics/mgc_illumina_s3_buckets.txt', 'r') as file:
		for line in file:
			line = line.rstrip('\n')
			command = (f'aws s3 ls s3://mgcdata/SS2/runs/{line}')
			command_output = run(['bash', '-c', command])
#			test_command = (f'aws s3 ls s3://mgcdata/SS2/runs/20181122/')
#			test_command_output = run(['bash', '-c', test_command])
			out = command_output.decode('utf8').split('\n')

			for i in out:
				sample_name = str(i.split(' ')[-1:]).lstrip("['").rstrip("']")
				if 'RSP' not in sample_name:
					if 'README' in sample_name:
						continue
					if 'md5' in sample_name:
						continue
					else:		
						print(f'{line}\t{sample_name}')


def main():
	query_s3()

if __name__ == '__main__':
	main()					