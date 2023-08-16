#!/usr/bin/env python3

# make_bar_plot.py

import argparse
import pandas as pd
from matplotlib import pyplot as plt

def parse_arguments():
    parser = argparse.ArgumentParser(description='Input the tsv file to produce a bar plot')
    parser.add_argument('-i', '--infile', help = 'TSV for analysis', required = True, dest = 'infile')
    parser.add_argument('-x', '--x_axis', help = 'Column for X axis', required = True, dest = 'x_axis')
    parser.add_argument('-y', '--y_axis', help = 'Column for Y axis', required = True, dest = 'y_axis')
    args = parser.parse_args()
    infile = args.infile
    x_axis = args.x_axis
    y_axis = args.y_axis
    return infile, x_axis, y_axis

def plot_data(file, x, y):
	
	data = pd.read_csv(file)
	df = pd.DataFrame(data)

	x_axis = df[x]
	y_axis = df[y]

	fig = plt.figure(figsize =(10, 7))

	plt.bar(x_axis, y_axis)

	plt.show()

def main():
	
	infile, x_axis, y_axis = parse_arguments()
	plot_data(infile, x_axis, y_axis)

if __name__ == '__main__':
	main()		     