#!/usr/bin/env python3

# parse_JL_gene_tsv.py

import csv
#import mysql.connector

def connect_to_db():
    import mysql.connector
    my_db = mysql.connector.connect(
        host = 'localhost',
        user = 'liam',
        password = 'liam',
        database = 'mgc',
        auth_plugin = 'mysql_native_password'
        )       
    return my_db

def sql_query(my_db):
    cursor = my_db.cursor()
    counter = 0
    with open('CoGe_id55184_Cannabis_sativa_Jamaican_Lion_Jamaican_Lion_Mother_Sorted_JLion_Final_061119.highQuality_models.EFWonly.tsv') as file:
        infile = csv.reader(file, delimiter="\t")
        for line in infile:
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
    sql_query(my_db)

if __name__ == '__main__':
    main()
