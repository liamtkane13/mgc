#!/usr/bin/env python3

# find_differences_between_gene_csvs.py

import pandas as pd

def compare_tsvs():
	
	rosetta_stone = pd.read_csv('JL_Mother-gene-details-even-more-detail-with-EFW-ID.tsv', sep='\t')

	old_rs = pd.read_csv('JL_Mother-gene-details-even-more-detail.tsv', sep='\t')

	efw_id_raw = pd.read_csv('CoGe_id55184_Cannabis_sativa_Jamaican_Lion_Jamaican_Lion_Mother_Sorted_JLion_Final_061119.highQuality_models.EFWonly.tsv', sep='\t')
	efw_df = efw_id_raw.drop(columns = ['ID', 'Gene'])

	old_rs_missing = (old_rs[~old_rs.mRNA_accession.isin(rosetta_stone.mRNA_accession)])
	efw_missing = (efw_df[~efw_df.Gene_EFW_ID.isin(rosetta_stone.Gene_EFW_ID)])
	old_rs_missing.to_csv('old_rs_samples_missing_EFW_ids.tsv', sep='\t')
	efw_missing.to_csv('EFW_samples_missing_corresponding_rs.tsv', sep='\t')	




def main():
	compare_tsvs()


if __name__ == '__main__':
	main()	