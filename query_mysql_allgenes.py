#!/usr/bin/env python3

# parse_JL_gene_tsv.py

import argparse
import sys
import csv

parser = argparse.ArgumentParser(description='Open gene list infile and search Kannapedia for variants in genes in infile.')
parser.add_argument('-i', '--infile', help='Gene list to query', required=True,dest='infile')
args = parser.parse_args()

def connect_to_db():
    import mysql.connector
    my_db = mysql.connector.connect(
        host = 'localhost',
        user = 'liam',
        password = 'liam',
        database = 'mgc',
        auth_plugin = 'mysql_native_password'
        )       
    return(my_db)

def infile_list():
    infile_counter = 0
    infile_list = []
    with open(args.infile, 'r') as infile:
        for line in infile:
            infile_counter += 1
            if infile_counter == 1:
                continue
            line = line.strip('\n')
            infile_list.append(line)
            print(infile_list)

def sql_query(my_db):
    cursor = my_db.cursor()
    counter = 0
    with open('CoGe_id55184_Cannabis_sativa_Jamaican_Lion_Jamaican_Lion_Mother_Sorted_JLion_Final_061119.highQuality_models.EFWonly.tsv') as file:
        gene_file = csv.reader(file, delimiter="\t")
        for line in gene_file:
            counter += 1
            if counter == 1: #skip header
                continue
            id = line[1]
            contig = line[3]
            start = line[4]
            stop = line[5]
            query = (f"select count(*) as count from cannsnp90_variants_annotated where contig= '{contig}' and (contig_pos >= {start} and contig_pos <= {stop})")
            cursor.execute(query)
            myresult = cursor.fetchall()
            for i in myresult:
                total_var = i[0]
                print(f'{id}\t{contig}\t{start}\t{stop}\t{total_var}')
def main():
    my_db = connect_to_db()
    infile_list()
#    sql_query(my_db)

if __name__ == '__main__':
    main()
