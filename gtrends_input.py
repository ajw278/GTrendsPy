from __future__ import print_function



"""
Fetch search terms from the file, but associate them in a dictionary
by line number
"""
def fetch_search_terms(fname):
	with open(fname) as f:
    		content = f.readlines()

	sterms = []
	sassoc = {}
	iass = 0
	for line in content:
		if len(line)>2:
			sassoc[iass] = []
			lsplit = line.split(',')
			for il in lsplit:
				sterms.append(il.strip())
				sassoc[iass].append(sterms[-1])

			iass+=1
		
	return sterms, sassoc



