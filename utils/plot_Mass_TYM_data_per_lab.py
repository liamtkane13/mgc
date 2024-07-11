#!/usr/bin/env python3

import argparse
import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib.cm import coolwarm 

def parse_arguments():
	parser = argparse.ArgumentParser(description='Input Mass TYM data per lab to plot')
	parser.add_argument('-i', '--infile', help = 'Mass TYM Data per lab to plot', required = True, dest = 'infile')
	args = parser.parse_args()
	infile = args.infile
	return infile

def plot_data(file):

	with open(file, 'r') as file:

		lab_x_counter = 0
		lab_x_pos_counter = 0

		lab_y_counter = 0
		lab_y_pos_counter = 0

		lab_z_counter = 0
		lab_z_pos_counter = 0

		lab_t_counter = 0
		lab_t_pos_counter = 0

		lab_a_counter = 0
		lab_a_pos_counter = 0

		lab_b_counter = 0
		lab_b_pos_counter = 0

		lab_e_counter = 0
		lab_e_pos_counter = 0

		lab_g_counter = 0
		lab_g_pos_counter = 0

		lab_h_counter = 0
		lab_h_pos_counter = 0

		lab_o_counter = 0
		lab_o_pos_counter = 0

		lab_p_counter = 0
		lab_p_pos_counter = 0

		lab_r_counter = 0
		lab_r_pos_counter = 0

		lab_s_counter = 0
		lab_s_pos_counter = 0																				

		for line in file:

			lab = line.split('\t')[4]
			result = line.split('\t')[3]

			if result == 'CFU':
				continue
			else:
				result = int(result)	

			if lab == 'LabX':

				lab_x_counter +=1

				if result >= 10000:

					lab_x_pos_counter +=1

			elif lab == 'LabY':

				lab_y_counter +=1

				if result >= 10000:

					lab_y_pos_counter +=1

			elif lab == 'LabZ':
				
				lab_z_counter +=1

				if result >= 10000:

					lab_z_pos_counter += 1

			elif lab == 'LabT':
				
				lab_t_counter +=1

				if result >= 10000:

					lab_t_pos_counter += 1

			elif lab == 'LabA':
				
				lab_a_counter +=1

				if result >= 10000:

					lab_a_pos_counter += 1

			elif lab == 'LabB':
				
				lab_b_counter +=1

				if result >= 10000:

					lab_b_pos_counter += 1

			elif lab == 'LabE':
				
				lab_e_counter +=1

				if result >= 10000:

					lab_e_pos_counter += 1

			elif lab == 'LabG':
				
				lab_g_counter +=1

				if result >= 10000:

					lab_g_pos_counter += 1

			elif lab == 'LabH':
				
				lab_h_counter +=1

				if result >= 10000:

					lab_h_pos_counter += 1

			elif lab == 'LabO':
				
				lab_o_counter +=1

				if result >= 10000:

					lab_o_pos_counter += 1

			elif lab == 'LabP':
				
				lab_p_counter +=1

				if result >= 10000:

					lab_p_pos_counter += 1

			elif lab == 'LabR':
				
				lab_r_counter +=1

				if result >= 10000:

					lab_r_pos_counter += 1	

			elif lab == 'LabS':
				
				lab_s_counter +=1

				if result >= 10000:

					lab_s_pos_counter += 1																																																						

		lab_x_fail_rate_raw = lab_x_pos_counter / lab_x_counter	
		lab_y_fail_rate_raw = lab_y_pos_counter / lab_y_counter	
		lab_z_fail_rate_raw = lab_z_pos_counter / lab_z_counter
		lab_t_fail_rate_raw = lab_t_pos_counter / lab_t_counter
		lab_a_fail_rate_raw = lab_a_pos_counter / lab_a_counter
		lab_b_fail_rate_raw = lab_b_pos_counter / lab_b_counter
		lab_e_fail_rate_raw = lab_e_pos_counter / lab_e_counter
		lab_g_fail_rate_raw = lab_g_pos_counter / lab_g_counter
		lab_h_fail_rate_raw = lab_h_pos_counter / lab_h_counter
		lab_o_fail_rate_raw = lab_o_pos_counter / lab_o_counter
		lab_p_fail_rate_raw = lab_p_pos_counter / lab_p_counter
		lab_r_fail_rate_raw = lab_r_pos_counter / lab_r_counter
		lab_s_fail_rate_raw = lab_s_pos_counter / lab_s_counter

		lab_x_fail_percentage = round((lab_x_fail_rate_raw *100), 2)
		lab_y_fail_percentage = round((lab_y_fail_rate_raw *100), 2)
		lab_z_fail_percentage = round((lab_z_fail_rate_raw *100), 2)
		lab_t_fail_percentage = round((lab_t_fail_rate_raw *100), 2)
		lab_a_fail_percentage = round((lab_a_fail_rate_raw *100), 2)
		lab_b_fail_percentage = round((lab_b_fail_rate_raw *100), 2)
		lab_e_fail_percentage = round((lab_e_fail_rate_raw *100), 2)
		lab_g_fail_percentage = round((lab_g_fail_rate_raw *100), 2)
		lab_h_fail_percentage = round((lab_h_fail_rate_raw *100), 2)
		lab_o_fail_percentage = round((lab_o_fail_rate_raw *100), 2)
		lab_p_fail_percentage = round((lab_p_fail_rate_raw *100), 2)
		lab_r_fail_percentage = round((lab_r_fail_rate_raw *100), 2)
		lab_s_fail_percentage = round((lab_s_fail_rate_raw *100), 2)

		print(f'LabX Fail Rate: {lab_x_fail_percentage}%')
		print(f'LabY Fail Rate: {lab_y_fail_percentage}%')
		print(f'LabZ Fail Rate: {lab_z_fail_percentage}%')
		print(f'LabT Fail Rate: {lab_t_fail_percentage}%')
		print(f'LabA Fail Rate: {lab_a_fail_percentage}%')
		print(f'LabB Fail Rate: {lab_b_fail_percentage}%')
		print(f'LabE Fail Rate: {lab_e_fail_percentage}%')
		print(f'LabG Fail Rate: {lab_g_fail_percentage}%')
		print(f'LabH Fail Rate: {lab_h_fail_percentage}%')
		print(f'LabO Fail Rate: {lab_o_fail_percentage}%')
		print(f'LabP Fail Rate: {lab_p_fail_percentage}%')
		print(f'LabR Fail Rate: {lab_r_fail_percentage}%')
		print(f'LabS Fail Rate: {lab_s_fail_percentage}%')


		data = [
			["LabX", lab_x_fail_percentage],
			["LabY", lab_y_fail_percentage],
			["LabZ", lab_z_fail_percentage],
			["LabT", lab_t_fail_percentage],
			["LabA", lab_a_fail_percentage],
			["LabB", lab_b_fail_percentage],
			["LabE", lab_e_fail_percentage],
			["LabG", lab_g_fail_percentage],
			["LabH", lab_h_fail_percentage],
			["LabO", lab_o_fail_percentage],
			["LabP", lab_p_fail_percentage],
			["LabR", lab_r_fail_percentage],
			["LabS", lab_s_fail_percentage],
		]	

		df = pd.DataFrame(data, columns = ['Lab', 'TYM Fail Rate%'])

		plot = df.plot.bar(x='Lab', y='TYM Fail Rate%')
		fig = plot.get_figure()
		fig.savefig("Mass_TYM_plot.png")

		print(f'\n\nLab\tFailed Tests\tTotal Tests')


		print(f'LabX\t{lab_x_pos_counter}\t{lab_x_counter}')
		print(f'LabY\t{lab_y_pos_counter}\t{lab_y_counter}')
		print(f'LabZ\t{lab_z_pos_counter}\t{lab_z_counter}')
		print(f'LabT\t{lab_t_pos_counter}\t{lab_t_counter}')
		print(f'LabA\t{lab_a_pos_counter}\t{lab_a_counter}')
		print(f'LabB\t{lab_b_pos_counter}\t{lab_b_counter}')
		print(f'LabE\t{lab_e_pos_counter}\t{lab_e_counter}')
		print(f'LabG\t{lab_g_pos_counter}\t{lab_g_counter}')
		print(f'LabH\t{lab_h_pos_counter}\t{lab_h_counter}')
		print(f'LabO\t{lab_o_pos_counter}\t{lab_o_counter}')
		print(f'LabP\t{lab_p_pos_counter}\t{lab_p_counter}')
		print(f'LabR\t{lab_r_pos_counter}\t{lab_r_counter}')
		print(f'LabS\t{lab_s_pos_counter}\t{lab_s_counter}')

		
def main():
	
	infile = parse_arguments()
	plot_data(infile)

if __name__ == '__main__':
	main()					