from __future__ import print_function

import os
import saveload as sl
import numpy as np
import copy
import operator
from collections import OrderedDict

import matplotlib.pyplot as plt

from pytrends.request import TrendReq



GROUPSIZE = 5


def fetch_resdict(query_list, trange, loc='GB'):
	PYTREND = TrendReq(hl='en-UK', tz=0)
	
	resdict = {}
	for query in query_list:
		if hasattr(query, '__iter__'):
			qtmp = list(query)
		else:
			qtmp = [query]
		print('Searching for:', qtmp)
		tmpdct1 = relative_data(qtmp, PYTREND, trange=trange,loc=loc)
		if not tmpdct1==None:
			if hasattr(query, '__iter__'):
				query = list(query)
				kw = ', '.join('"'+query+'"')
				composite = np.zeros(len(tmpdct1['Date']))
				for q in query:
					composite+=tmpdct1[q]
				composite *= 100./np.amax(composite)
				tmpdct = {}
				tmpdct[kw] = composite
				tmpdct['Date'] = tmpdct1['Date']
			else:
				kw = '"'+query+'"'
				tmpdct = tmpdct1
			resdict[kw] = [tmpdct[kw], tmpdct['Date']]
			
		else:
			if type(query)==list:
				kw = ', '.join('"'+query+'"')
			else:
				kw = query
			resdict[kw] = None
		

	return resdict


"""
Note:
Google trends data is already relative for time period an location.
"""

def relative_data(query_list, pytrend, trange='today 5-y', loc='GB'):

	pytrend.build_payload(query_list, cat=0, timeframe=trange, geo=loc, gprop='')

	trend = pytrend.interest_over_time()
	#trend(trend_payload, return_type='dataframe')
					
	data_dict = {}
	icol = 0
	for key in trend.columns:
		icol+=1
		if not key==u'isPartial':
			data_dict[key] = list(trend.loc[:,key])

	if icol==0:
		print('No data found for:', query_list)
		return None


	data_dict['Date'] = list(trend.index.values)
	#nentried = len(data_dict['Date'])
	#print('Number of entries found: ', nentries)

	return data_dict



def query_ranges(query_list, date_list, window_days, resdict=None, loc='GB'):

	if resdict==None:
		PYTREND = TrendReq(hl='en-UK', tz=0)

	tdiff = np.timedelta64(int(window_days/2),'D')
	dfracs = []
	qfinal = []
	iq =0
	tmpdct=None


	for query in query_list:
		d2 = date_list[iq]+tdiff
		d1 =  date_list[iq]-tdiff
		d1 = str(d1)[:10]
		d2 = str(d2)[:10]
		dstring = d1+' '+d2

		if hasattr(query, '__iter__'):
			kw = ', '.join(query)
		else:
			kw = query

		if resdict==None:
			if hasattr(query, '__iter__'):
				qtmp = list(query)
			else:
				qtmp = [query]
			print('Searching for:', qtmp)
			tmpdct1 = relative_data(qtmp, PYTREND, trange=dstring, loc=loc)
			if hasattr(query, '__iter__') and tmpdct1!=None:
				query= list(query)
				kw = ', '.join(query)
				composite = np.zeros(len(tmpdct1['Date']))
				for q in query:
					composite+=tmpdct1[q]
				composite *= 100./np.amax(composite)
				tmpdct = {}
				tmpdct[kw] = composite
				tmpdct['Date'] = tmpdct1['Date']
			elif hasattr(query, '__iter__'):
				kw = ', '.join(query)
				tmpdct = tmpdct1
			else:
				kw = query
				tmpdct = tmpdct1
			#EDITING HERE!!!

			#resdict[query] = [tmpdct[query], tmpdct['Date']]
			if not tmpdct==None:
				dfracs.append(diff_frac(tmpdct[kw], tmpdct['Date'], date_list[iq], window_days))
				qfinal.append(query)
		elif kw in resdict:
			if resdict[kw]!=None:
				dfracs.append(diff_frac(resdict[kw][0], resdict[kw][1], date_list[iq], window_days))
				qfinal.append(query)

					
		iq+=1

	return qfinal, dfracs



def get_reference(dataset):
	klist = []
	mlist = []
	for key in dataset:
		if key!='Date':
			klist.append(key)
			mlist.append(np.amax(np.asarray(dataset[key])))

	mlist = np.array(mlist)
	ref_index = np.argsort(mlist)[len(mlist)//2]
	
	return klist[ref_index]


def find_lowfactors(global_dict, qlist, thresh=1e-7):

	iquers = []

	iq =0
	for quer in qlist:
		if global_dict[qlist[iq]]['factor']<=thresh*1.0001:
			iquers.append(iq)
		iq+=1

	
		

	return np.array(iquers, dtype=int)

def sort_queries(queries, factors):

	allfacts = np.array(factors)
	allquers = np.array(queries)
	
	qsort = np.argsort(allfacts)
	allquers = allquers[qsort][::-1]
	
	return allquers

	
	



def pairwise_queryset(global_dict, query_set, trange, fname, ptrend=None, loc='GB', tol=1e-1):
	MaxLoop = len(global_dict)
	ref_fact = 1.0
	allfacts_pw = np.ones(len(query_set))*ref_fact
	ipair =0
	notSorted=True
	cmp2ext = '_2comp'


	allquers = []
	allfacts = []
	
	print('Data comparison before pairwise sweep:')
	print('Query    Factor    Approx?')

	for quer in query_set:
		allfacts.append(global_dict[quer]['factor'])
		allquers.append(quer)

	allquers = sort_queries(allquers, allfacts)


	global_dict3 = {}

	if os.path.exists('obj/'+fname+cmp2ext+'.pkl'):
		print('Loading previous for 2 comparison file...')
		global_dict3 = sl.load_obj(fname+cmp2ext)

	
	
	allquers_prev = allquers
	iqueries = np.arange(len(allquers))
	iqsrt = iqueries
	iqsrt_prev = iqueries

	tmp_dict = {}
	for q in allquers:
		tmp_dict[q] = global_dict[q]['factor']

	srt_pw_dict =  OrderedDict(sorted(tmp_dict.items(), key=operator.itemgetter(1), reverse=True))
	srt_pw_list = []
	for key in srt_pw_dict:
		srt_pw_list.append(key)

	
	data_warning = {}
	while notSorted and ipair<MaxLoop:

		print('Pairwise sweep %d/%d'%(ipair+1, MaxLoop))
		
		srt_pw_list_prev = copy.copy(srt_pw_list)

		srt_pw_dict[srt_pw_list[0]] =1.

		#Loop through query indices, sorted into descending popularity
		for iiq in range(len(srt_pw_list)-1):
			
			if ptrend==None:
				ptrend = TrendReq(hl='en-UK', tz=0)

			quer = srt_pw_list[iiq]
			next_quer =  srt_pw_list[iiq+1]


			qstring = str(quer)+", "+str(next_quer)
			qtmp = [quer, next_quer]

			if not qstring in global_dict3:
				print('Requesting data for: ', qstring)
				
				global_dict3[qstring] = {'data': relative_data(qtmp, ptrend, trange=trange, loc=loc), 'factor':1.0}

				sl.save_obj(global_dict3, fname+cmp2ext)

			
			q1sum = float(sum(global_dict3[qstring]['data'][qtmp[0]]))
			q2sum = float(sum(global_dict3[qstring]['data'][qtmp[1]]))


			if q2sum/(q1sum+1e-10)>100. or q2sum/(q1sum+1e-10)<0.01:
				print('Error: pairwise comparison yielded a drop fraction greater than 100')
				print('Comparison terms: {0} vs. {1}'.format(qtmp[0], qtmp[1]))
				print('\n**********\nData 1:', global_dict3[qstring]['data'][qtmp[0]])
				print('\n**********\nData 2:', global_dict3[qstring]['data'][qtmp[1]])
				exit()

			#If the next query is much more popular than the previous then swap. 
			if q2sum>1.1*q1sum:
				print('Swapping: %s with %s (ratio: %.2lf)'%(quer, next_quer, q2sum/q1sum))
				srt_pw_list[iiq], srt_pw_list[iiq+1] = srt_pw_list[iiq+1], srt_pw_list[iiq]
				q1sum, q2sum = q2sum, q1sum
				srt_pw_dict[srt_pw_list[iiq]] = 1.

				if ipair>120:
					plt.plot(global_dict3[qstring]['data']['Date'], global_dict3[qstring]['data'][quer])
					plt.plot(global_dict3[qstring]['data']['Date'], global_dict3[qstring]['data'][next_quer])
					plt.show()
			
			srt_pw_dict[srt_pw_list[iiq+1]] = q2sum/q1sum

			
			
			qtmp = []
	

		notSorted=False
		if srt_pw_list_prev!=srt_pw_list:
			notSorted=True
		
		ipair+=1

		if ipair >= MaxLoop:
			print('Warning: reached maximum number of sweeps for pairwise comparison without success')
			print('Using current data, but discrepancies between comparisons exist.')
			

	print('Pairwise sweep complete..')

	factor=1.0
	
	for item in srt_pw_list:
		factor*= srt_pw_dict[item]
		global_dict[item]['factor'] = factor
		global_dict[item]['f_approx'] = False
		print(item, global_dict[item]['factor'] )



	sl.save_obj(global_dict, fname)

	return global_dict, global_dict3	


"""
relative_queryset 
At present, this function does all of the analysis by compairing in groups and
pairwise different queries to give a 'factor' associated with each giving its
relative number of searches compared to other terms. 
"""
def relative_queryset(all_queries, fname, trange, qassoc=None, loc='GB', verbose=False):
	cmpext = '_5comp'

	print('Beginning relative queryset compilation...')
	
	PYTREND=None

	if not os.path.isdir('obj'):
		os.makedirs('obj')
	if os.path.exists('obj/'+fname+'.pkl'):
		print('Loading previous file...')
		global_dict = sl.load_obj(fname)
	else:
		global_dict = {}
		sl.save_obj(global_dict, fname)
	if type(all_queries)==str:
		query_elements = all_queries.split(', ')
	elif type(all_queries)==list:
		query_elements = all_queries
	else:
		print("Data type for query input must be 'list' or 'string'")
		exit()
	

	if verbose:
		print('Query elements: ', query_elements)


	"""
	global_dict is the main dictionary - all search terms are stored individually here, including
	their relative factor
	
	First just loop through the queries and search for each in pytrends
	"""
	for query in query_elements:
		if not query in global_dict:
			if PYTREND==None:
				PYTREND = TrendReq(hl='en-UK', tz=0)
			print('Requesting data for: ', query)
			global_dict[query] = {'data':relative_data([query], PYTREND, trange=trange, loc=loc), 'factor':.0}
			sl.save_obj(global_dict, fname)
			#print('Data for %s saved successfully.' %query)
			#Need to wait so as not to exceed google's rate limit
			#time.sleep(random.randint(1, 4))
		else:
			print('"%s" already stored in dictionary.' %query)


	"""
	del_queries - queries for which there is no data

	go through the global_dict and check if there is data
	"""
	del_queries = []
	
	for qu in global_dict:
		if global_dict[qu]['data']==None:
			del_queries.append(qu)


	"""
	global_dict2 is a dictionary in which 5 search terms are compared
	at once. By applying a 'reference term', each 5 are compared to each
	other 5. 

	"""

	
	#Remove queries which we do not want.
	query_set = [q for q in global_dict if q not in del_queries]

	query_comps = []
	iqueries = range(len(query_set))
	Nlow  = 1
	lq_val = 1e-7
	MaxLoops = 5

	icheck = 0

	#Try to load old versions of the 5 query comparison
	if os.path.exists('obj/'+fname+cmpext+'.pkl'):
		print('Loading previous for 5 comparison file...')
		global_dict2 = sl.load_obj(fname+cmpext)
		iqueries = find_lowfactors(global_dict, query_set, thresh=lq_val)
	else:
		global_dict2 = {}
		#sl.save_obj(global_dict, fname+cmpext)


	#query_set = copy.copy(query_elements)
	#ESTABLISH PLAN BEFORE CONTINUING... REWRITE!!!
	if not 'REF' in global_dict2:
		global_dict2['REF'] = ''
		sl.save_obj(global_dict2, fname+cmpext)

	ref_query = global_dict2['REF']
			


	"""
	At present, this is pretty rough - I simply set search terms which have '0' searches
	relative to the other terms to a small number (1e-7) for the subsequent pairwise 
	comparison (which is the one thats important to get right...)

	"""

	while len(iqueries)>Nlow and icheck<MaxLoops:

		print('Five query check, loop number %d/%d'%(icheck+1, MaxLoops))
		query_temp = []
		subiquery=0
		for iquery in iqueries:
			query_temp.append(query_set[iquery])
			#If there is not a reference query then we need to strip the first 5 queries
			#If there is a reference query already, can simply divide the queries into 4s
			if ref_query=='':
				groupsize = GROUPSIZE
			else:
				groupsize = GROUPSIZE-1
			if len(query_temp)%groupsize==0 or iquery==len(query_set)-1:
				if not ref_query == '':
					query_temp.append(ref_query)
				qstring = ", ".join(query_temp)

				if PYTREND==None:
					PYTREND = TrendReq(hl='en-UK', tz=0)

				if not qstring in global_dict2:
					print('Requesting data for: ', qstring)
					global_dict2[qstring] = {'data': relative_data(query_temp, PYTREND, trange=trange, loc=loc), 'factor':1.0}
					
				if ref_query == '':
					ref_query = get_reference(global_dict2[qstring]['data'])
					global_dict2['REF']=ref_query
				if not qstring in global_dict2:
					sl.save_obj(global_dict2, fname+cmpext)

				for quer in query_temp:
					if max(global_dict2[qstring]['data'][ref_query])>1e-7:
						global_dict[quer]['factor'] = float(max(global_dict2[qstring]['data'][quer]))/float(max(global_dict2[qstring]['data'][ref_query]))
					else:
						global_dict[quer]['factor'] =lq_val

					
					global_dict[quer]['f_approx'] = True
						
				query_temp = []

		iqueries = find_lowfactors(global_dict, query_set, thresh=lq_val)
		
		if len(iqueries)>Nlow and icheck>=MaxLoops:
			print('Error: Number of sweeps for the 5 query comparison exceeded')
			print('Number of queries below limit: %d/%d'%(len(iqueries)/len(global_dict)))
			exit()

		icheck+=1
		
	sl.save_obj(global_dict, fname)
	


	"""
	global_dict3 is where the pairwise comparison happens
	
	Problem: low search terms presently cannot be ordered for the
	pairwise comparison. Might fail to get correct scaling at the 
	low popularity end. Probably need to add a number of loops in
	which global_dict2 is refined for queries where factor==1e-7

	"""
	global_dict, global_dict3 = pairwise_queryset(global_dict, query_set, trange,fname, ptrend=PYTREND,loc=loc)
	
			

	
	return global_dict, global_dict2, global_dict3




