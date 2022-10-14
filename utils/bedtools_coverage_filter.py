#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Provide txt files of bedtools genomecov output for filtering')
parser.add_argument('-i', '--infile', help='Coverage list to filter', required=True,dest='infile')
args = parser.parse_args()

def look_at_file(infile):
    with open(infile, 'r') as file:
        for line in file:
           coverage = int(line.split('\t')[2])
           if coverage > 1000:
               print(line)

def main():
    cov_file = args.infile
    look_at_file(cov_file)

if __name__ == '__main__':
    main()
