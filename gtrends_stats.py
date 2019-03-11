from __future__ import print_function

import numpy as np



#Arguments: searches array, datetime array, split of dates, total window size in days
def diff_frac(nsearch_list, date_list, dsplit, window_days):
	tdiff = np.timedelta64(int(window_days/2.),'D')
	tmax = dsplit+tdiff
	tmin = dsplit-tdiff
	dates =np.array(date_list)
	nsearch = np.array(nsearch_list)
	after_inds = np.where((dates.astype('datetime64[D]') < tmax.astype('datetime64[D]'))&(dates.astype('datetime64[D]') >= dsplit.astype('datetime64[D]')))[0]

	before_inds = np.where((dates.astype('datetime64[D]') >= tmin.astype('datetime64[D]'))&(dates.astype('datetime64[D]') < dsplit.astype('datetime64[D]')))[0]

	all_inds = np.where((dates.astype('datetime64[D]') >= tmin.astype('datetime64[D]'))&(dates.astype('datetime64[D]') < tmax.astype('datetime64[D]')))[0]

	after_val = np.mean(nsearch[after_inds])	

	before_val = np.mean(nsearch[before_inds])

	pchange = 100.*(after_val-before_val)/before_val

	print('Percentage Change:', pchange)
 
	return pchange
