#!/usr/bin/env python3

# add_EFW_ID_to_mRNA_csv_pandas.py

import pandas as pd

def crunch_tsvs():
	efw_df_raw = pd.read_csv('CoGe_id55184_Cannabis_sativa_Jamaican_Lion_Jamaican_Lion_Mother_Sorted_JLion_Final_061119.highQuality_models.EFWonly.tsv', sep='\t')
	efw_df = efw_df_raw.drop(columns = ['ID', 'Gene'])
	rs_df = pd.read_csv('JL_Mother-gene-details-even-more-detail.tsv', sep='\t')
	complete_df = pd.merge(rs_df, efw_df, on = ['Contig', 'start', 'stop'])
	complete_df.to_csv('JL_Mother-gene-details-even-more-detail-with-EFW-ID_pandas.tsv', sep='\t', header=True, index=False) 


def main():
	crunch_tsvs()

if __name__ == '__main__':
	main()	