#!/usr/bin/env python3

import argparse
import subprocess
import statistics
import glob
import csv 
from subprocess import Popen, PIPE

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input BAM files for samtools depth, to be output as a tsv file')
	parser.add_argument('-i', '--infiles', nargs = '+', help = 'BAM files for samtools', required = True, dest = 'infiles')
	parser.add_argument('-s', '--sample_sheet', help = 'Sample Sheet for naming', dest = 'sample_sheet')
	args = parser.parse_args()
	matched_files = []
	for file in args.infiles:
		if glob.escape(file) != file:
			matched_files.extend(glob.glob(file))
		else:
			matched_files.append(file)
	return matched_files, args.sample_sheet	


def make_name_dictionary(samplesheet):
	name_dictionary = {}
	with open(samplesheet, 'r')	as file:
		reader = csv.reader(file)
		for line in reader:
			name_dictonary = {line[3]:line[0]}
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

	header = '<table id="myTable" class="table table-striped table-bordered" style="width:100%"><thead><tr><th>Sample Name</th><th>Reference Name</th><th>C10</th><th>C30</th><th>Percent Bases Uncovered</th><th>Median Coverage</th><th>Mean Coverage</th><th>IGV Link</th></tr></thead>'
	html_table.append(header)

	for file in files:

		overall = 0
		cov_10 = 0
		cov_30 = 0
		uncov_bases = 0
		coverage_list = []


		barcode_name = file.split('-')[0].split('code')[1]
		print(barcode_name)
		sample_name = dictionary[barcode_name]
		ref_name = file.split('REF_')[1].split(':')[0]
		contig_name = file.split('REF_')[1].split('.bam')[0]
		bam_igv_raw = file.split('REF_')[0]
		bam_igv = (f'{bam_igv_raw}bam')

		igv_link = (f'http://localhost:60151/load?file=https://mgcdata.s3.amazonaws.com/shared/igv-links/ONT_ref_coverage/{bam_igv}&locus={contig_name}&genome=https://mgcdata.s3.amazonaws.com/shared/ref/Nanopore_TYM_and_Rockefeller_Amplicons_3.fasta') 


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
			html_line = (f'<tr><td>{sample_name}</td><td>{ref_name}</td><td>{C10}</td><td>{C30}</td><td>{uncov_percent}</td><td>{median_cov}</td><td>{mean_cov}</td><td><a target="_blank" href="{igv_link}">IGV_Link</a></td></tr>')
			html_table.append(html_line)

	html_table.append('</table>')
	for it in html_table:
		print(it)


def main():
	matched_files, sample_sheet = parse_arguments()
	name_dictionary = make_name_dictionary(sample_sheet)
	run_samtools(matched_files, name_dictionary)


if __name__ == "__main__":
	main()