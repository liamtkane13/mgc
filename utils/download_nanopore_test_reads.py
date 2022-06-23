#!/usr/bin/env python3

# download_nanopore_test_reads.py

import json
import subprocess


def make_download_file():
    with open('filereport_read_run_PRJEB51164_json.txt') as file:
        for line in file:
            if 'r10.4' in line:
                split_line = line.split(',')
                for i in split_line:
                    if '"submitted_ftp"' in i:
                        ftp = i.split('"')[3]
                        print(ftp)
                        


def main():
    make_download_file()

if __name__ == '__main__':
    main()
