#h !/usr/bin/env python3

# find_redundant_bams_on_s3.py

from subprocess import check_output as run 

def make_batch_list():

	ls_command = (f'aws s3 ls s3://mgcdata/production/Dragen/')
	ls_output = (run(['bash', '-c', ls_command])).decode('utf8')

	batch_list = []

	batch_raw = ls_output.split('PRE ')

	for i in batch_raw:

		batch_date = i.split("\n")[0]
		batch_list.append(batch_date)

#	If anyone ever sees this BS move, I am truly sorry. 

	batch_list.pop(0)
	batch_list.pop(0)
	batch_list.pop()
	batch_list.pop()

	return batch_list 

def compare_bam_hashes(b_list):

	for batch in b_list:

		ls_command = (f'aws s3 ls s3://mgcdata/production/Dragen/{batch}')
		ls_output = ((run(['bash', '-c', ls_command])).decode('utf8')).split('\n')

		for i in ls_output:

			if '.bam' in i:

				name = str(i.split(' ')[-1])

				if "bai" in name:
					continue

				elif "md5sum" in name:
					continue

				else:

					production_link = (f's3://mgcdata/production/Dragen/{batch}{name}')
					public_link = (f's3://mgcdata/SS2/bams/public/{name}')

					samtools_production_command = (f"samtools view {production_link} -H | grep -v 'samtools view' | md5sum")
					samtools_public_command = (f"samtools view {public_link} -H | grep -v 'samtools view' | md5sum")

					production_hash = (run(['bash', '-c', samtools_production_command])).decode('utf8')
					public_hash = (run(['bash', '-c', samtools_public_command])).decode('utf8')

					if public_hash == production_hash:
						print(f'{name} is a redundant BAM file')
						prune_command = (f'aws s3 rm {production_link}')
						print(prune_command)





	

def main():

	batch_list = make_batch_list()
	compare_bam_hashes(batch_list)



if __name__ == '__main__':
	main()	