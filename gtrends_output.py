from __future__ import print_function

import csv
import numpy as np


def relative_searches_csv(global_dict, qassoc, outname):

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
						str_tmp.append(global_dict[qassoc[iq][iv]]['factor'])
						stot+= global_dict[qassoc[iq][iv]]['factor']
					else:
						str_tmp.append(qassoc[iq][iv])
						str_tmp.append(0)

				if iv==2:
					str_tmp.append('')
					str_tmp.append('')

				str_tmp.append(stot)

				writer.writerow(str_tmp)


	return None


def individual_searches_csv(global_dict, qassoc, outname):

	str_list = []

	Dates = None
	for key in global_dict:
		if Dates==None:
			Dates = global_dict[key]['data']['Date']
	
	

	with open(outname+'.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		COLS = ['Search term'] +['Association'] + ['Factor']
		for date in Dates:
			COLS+=[date]
		
		writer.writerow(COLS)
		
				
		if not qassoc==None:
			for iq in qassoc:

				for iv in range(len(qassoc[iq])):
					
					str_tmp = []
					str_tmp.append(qassoc[iq][iv])
					str_tmp.append(iq)
					str_tmp.append(global_dict[qassoc[iq][iv]]['factor'])
					if type(global_dict[qassoc[iq][iv]]['data'])!=type(None):
						str_tmp += list(global_dict[qassoc[iq][iv]]['data'][qassoc[iq][iv]])
					writer.writerow(str_tmp)


	return None
