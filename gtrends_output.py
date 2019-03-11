from __future__ import print_function

import csv
import numpy as np


def write_to_csv(global_dict, qassoc, outname):

	str_list = []

	stot_all = []
	if not qassoc==None:
		for iq in qassoc:
			str_tmp = ''
			stot=0.0
			for iv in range(len(qassoc[iq])):
				if 'factor' in global_dict[qassoc[iq][iv]]:
					str_tmp+=qassoc[iq][iv]+': '+str(global_dict[qassoc[iq][iv]]['factor'])+' '
					stot+= global_dict[qassoc[iq][iv]]['factor']
				else:
					print('Factor not in dictionary:', qassoc[iq][iv])
					str_tmp+=qassoc[iq][iv]+': 0 '
			str_tmp += 'TOTAL: '+str(stot)
			stot_all.append(stot)
				
			str_list.append(str_tmp)
	
	stot_all = np.array(stot_all)
	norm_fact = np.median(stot_all)

	with open(outname+'.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(['Term 1'] +['Searches']+ ['Term 2'] + ['Searches']+  ['Term 3'] + ['Searches']+  ['Term 4'] + ['Searches']+['Total'])
		
				
		if not qassoc==None:
			for iq in qassoc:
				str_tmp = []
				stot = 0.0


				for iv in range(len(qassoc[iq])):
					if 'factor' in global_dict[qassoc[iq][iv]]:
						
						str_tmp.append(qassoc[iq][iv])
						str_tmp.append(global_dict[qassoc[iq][iv]]['factor']/norm_fact)
						stot+= global_dict[qassoc[iq][iv]]['factor']
					else:
						str_tmp.append(qassoc[iq][iv])
						str_tmp.append(0)

				if iv==2:
					str_tmp.append('')
					str_tmp.append('')

				str_tmp.append(stot/norm_fact)

				writer.writerow(str_tmp)


	return None

