from __future__ import print_function

import matplotlib.pyplot as plt


def pie_chart(names, vals):
	sizes = 100.*vals/(np.sum(vals))
	plt.pie(sizes,  labels=names, autopct='%1.1f%%', startangle=90)
	plt.show()

def cumdist(list_cums, lab_list, label=None):

	plt.figure(figsize=(4.0, 4.))

	for icum in range(len(list_cums)):
		X = list_cums[icum]
		n = np.arange(1,len(X)+1) / np.float(len(X))
		Xs = np.sort(X)
		Xs = np.append(np.array([Xs[0]]), Xs)
		n = np.append(np.array([0.0]), n)
		plt.step(Xs,n, label=lab_list[icum]) 
		#n, bins, patches = plt.hist(list_cums[icum], 50, normed=1, histtype='step',
		#           cumulative=True, label=lab_list[icum])

	if not label==None:
		plt.text(0.0, 0.25, label)

	plt.ylim([0.,1.])
	#plt.xlim([-2.5,2.5])
	plt.legend(loc=4)
	plt.ylabel('Cumulative Fraction')
	plt.xlabel('$\%$ Search Increase (6 month)')

	plt.savefig('cumdist_6mo_bf.pdf', bbox_inches='tight', format='pdf')

	plt.show()
