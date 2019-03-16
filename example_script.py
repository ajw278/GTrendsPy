from __future__ import print_function

import gtrends_class as gtc
import numpy as np

TSTART = np.datetime64('2005-01-01')
TEND = np.datetime64('2018-01-01')

d1 = str(TSTART)[:10]
d2 = str(TEND)[:10]
dstring = d1+' '+d2

T_RANGE = dstring #'2006-12-14 2017-01-25'

INFILE = 'search_terms.dat'

OUTNAME = 'test'


plot_queries = ['Celastrina argiolus', 'Peacock', 'Comma', 'Marbled white butterfly']

tcomp = np.datetime64('2016-01-01')


if __name__=='__main__':
	#Set up google trends object with all the queries you want and the time range, geography etc.
	trend_obj = gtc.gtrends_dataset(OUTNAME, INFILE, T_RANGE, load=True, force_analysis=False, location='GB')

	trend_obj.output2csv()

	trend_obj.plot_tseries(plot_queries)


	trend_obj.get_ratio_ba(plot_queries[1], tcomp)

	
	
	
