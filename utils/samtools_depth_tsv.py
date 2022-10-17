#!/usr/bin/env python3

import argparse
import subprocess
import statistics
import glob 
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description='Input BAM files for samtools depth, to be output as a tsv file')
parser.add_argument('-i', '--infiles', nargs = '+', help = 'BAM files for samtools', required = True, dest = 'infiles')
args = parser.parse_args()

def make_name_dictionary():
	name_dictionary = {
		'barcode28' : 'MGC_A1_ITS',
		'barcode33' : 'MGC_C1_ITS',
		'barcode34' : 'D1_Direct_ITS',
		'barcode35' : 'D2_Direct_ITS',
		'barcode37' : 'D3_Direct_ITS',
		'barcode38' : 'D4_Direct_ITS',
		'barcode39' : 'MGC_A1_ROCK',
		'barcode40' : 'MGC_C1_ROCK',
		'barcode41' : 'D1_Direct_ROCK',
		'barcode42' : 'D2_Direct_ROCK',
		'barcode43' : 'D3_Direct_ROCK',
		'barcode44' : 'D4_Direct_ROCK'
	}
	return name_dictionary

def run_samtools(files, dictionary):

	html_table = []
	
	html_table.append("<head>")
	intro_line = '<script src="https://code.jquery.com/jquery-3.5.1.js"></script>'
	intro_line1 = '<script src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"></script>'
	intro_line2 = '<script src="https://cdn.datatables.net/1.12.1/js/dataTables.bootstrap4.min.js"></script>'
	link_line1 = '<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'
	link_line2 = '<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/dataTables.bootstrap.min.css">'
	html_table.append(link_line1)
	html_table.append(link_line2)
	html_table.append(intro_line)
	html_table.append(intro_line1)
	html_table.append(intro_line2)
	html_table.append("</head>")
	html_table.append("<script>")
	function = "$(document).ready( function () { \
		$('#myTable').DataTable(); \
	} )" 

	html_table.append(function)
	html_table.append("</script>")	

	header = '<table id="myTable" class="table table-striped table-bordered" style="width:100%"><thead><tr><th>Sample_Name</th><th>Reference_Name</th><th>C10</th><th>C30</th><th>Percent_Bases_Uncovered</th><th>Median_Coverage</th><th>Mean_Coverage</th><th>IGV_Link</th></tr></thead>'
	html_table.append(header)

	for file in files:

		overall = 0
		cov_10 = 0
		cov_30 = 0
		uncov_bases = 0
		coverage_list = []


		barcode_name = file.split('-')[0]
		sample_name = dictionary[barcode_name]
		ref_name = file.split('REF_')[1].split(':')[0]
		bam_igv_raw = file.split('REF_')[0]
		bam_igv = (f'{bam_igv_raw}bam')

		igv_link = (f'http://localhost:60151/load?file=http://mgcdata.s3.amazonaws.com/shared/igv-links/ONT_ref_coverage/{bam_igv}&genome=http://mgcdata.s3.amazonaws.com/shared/ref/Nanopore_TYM_and_Rockefeller_Amplicons_3.fasta') 


		command = (f"samtools depth -a {file}")
		output = Popen(['bash', '-c', command], stdout=PIPE)
			
		for line in output.stdout:
			try:

				overall += 1
				line = line.decode('utf8')
				coverage = line.split('\t')[2]
				coverage_list.append(int(coverage))
			
				if int(coverage) >= 10:
					cov_10 += 1
				if int(coverage) >= 30:
					cov_30 += 1	
				if int(coverage) == 0:
					uncov_bases += 1	
					
			except:
				continue		 
		if overall > 0:		
			C10 = cov_10 / overall
			C10 = round(C10, 2)
			C30 = cov_30 / overall
			C30 = round(C30, 2)
			uncov_percent = uncov_bases / overall
			uncov_percent = round(uncov_percent, 2)
			median_cov = statistics.median(coverage_list)
			median_cov = round(median_cov, 2)
			mean_cov = statistics.mean(coverage_list)
			mean_cov = round(mean_cov, 2)

		else:
			C10 = 0.0
			C30 = 0.0

		if cov_10 > 0:		
#			print(f'{sample_name}\t{ref_name}\t{C10}\t{C30}\t{uncov_percent}\t{median_cov}\t{mean_cov}\t{igv_link}')  
			html_line = (f'<tr><td>{sample_name}</td><td>{ref_name}</td><td>{C10}</td><td>{C30}</td><td>{uncov_percent}</td><td>{median_cov}</td><td>{mean_cov}</td><td><a target="_blank" href="{igv_link}">IGV_Link</a></td></tr>')
			html_table.append(html_line)

	html_table.append('</table>')
	print(html_table)

def main():
	infiles = args.infiles
	infiles = glob.iglob(infiles, recursive=True)
	name_dictionary = make_name_dictionary()
	run_samtools(infiles, name_dictionary)


if __name__ == "__main__":
	main()