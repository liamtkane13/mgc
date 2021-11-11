#!/usr/bin/env python3

# parse_JL_gene_tsv.py

import csv
import mysql.connector

my_db = mysql.connector.connect(
        host = 'localhost',
        user = 'liam',
        password = 'liam',
        database = 'mgc',
        auth_plugin = 'mysql_native_password'
)        

cursor = my_db.cursor()

def sql_query():
    with open('CoGe_id55184_Cannabis_sativa_Jamaican_Lion_Jamaican_Lion_Mother_Sorted_JLion_Final_061119.highQuality_models.EFWonly.tsv') as file:
        infile = csv.reader(file, delimiter="\t")
        for line in infile:
            id = line[1]
            contig = line[3]
            start = line[4]
            stop = line[5]
            print(f'{id}\t{contig}\t{start}\t{stop}')
            query = (f"select count(*) as count from cannsnp90_variants_annotated where contig= '{contig}' and (contig_pos >= {start} and contig_pos <= {stop})")
#            cursor.execute(query)
            print(query)
def main():
    sql_query()

if __name__ == "__main__":
    main()
