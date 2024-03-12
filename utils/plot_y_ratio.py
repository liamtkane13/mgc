#!/usr/bin/env python3

# plot_y_ratio.py

import argparse
import matplotlib.pyplot as plt
from matplotlib.cm import coolwarm
import pandas as pd


def parse_arguments():
	parser = argparse.ArgumentParser(description='Input the samtools idxstats Y ratio output file for plotting')
	parser.add_argument('-i', '--infile', help = 'Y ratio file', required = True, dest = 'infile')
	args = parser.parse_args()
	infile = args.infile
	return infile


def plot_y_ratios_pandas(file):
	
	ratio_df = pd.read_csv(file, sep='\t')	
	y_only_df = ratio_df.drop(columns=['Total Mapped', 'Total Y Mapped'])

	print(y_only_df)

	plot = ratio_df.plot.scatter(x='RSP', y='Y Ratio')
	fig = plot.get_figure()
	fig.savefig("y_ratio_plot.png")


def main():
	
	infile = parse_arguments()
	plot_y_ratios_pandas(infile)

if __name__ == '__main__':
	main()				