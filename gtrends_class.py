from __future__ import print_function

#Python distribution modules
import os
import numpy as np

#The following modules are written for this code:
import saveload as sl
import gtrends_input as gtinput
import gtrends_utilities as gtutils
import gtrends_output as gtout
import gtrends_plot as gtplot




class gtrends_dataset():
	def __init__(self, name, infile_name, trange, load=True, force_analysis=False, location='GB'):
		
		self.name = name
		self.infile = infile_name
		self.trange = trange
		self.location = location
		self.complete =False

		if self.check_previous() and not load:
			print('Previous version found, but load not requested.')
			print('Please remove/rename previous version before continuing')
			exit()
		elif self.check_previous() and load:
			print('Loading previous gtrends object "{0}"'.format(self.name))
			self.load()
			print('Complete:', self.complete)
		else:
			self.save()
			
		if not self.complete or force_analysis:
			self.get_input()
			self.main()
			self.complete = True
			self.save()

		return None


	def add_term(self, search_terms, assocs=None):
		print('add_term not implemented yet...')
		exit()
		return None
	

	def delete_term(self, search_term):
		print('delete_term not implemented yet...')
		exit()
		return None

	
	def check_previous(self):
		return os.path.isfile('obj/'+self.name+'.gtr.pkl')



	def save(self):
		if not os.path.isdir('obj'):
			os.makedirs('obj')
		
		sl.save_obj(self, self.name+'.gtr')
		

	def load(self):
		if self.check_previous():
			prev = sl.load_obj(self.name+'.gtr')
			attr = prev.__dict__
			for key in attr:
				setattr(self, key, attr[key])

		else:
			print('Error: load call failure, file not found.')
			
			exit()
		
	
	def get_input(self):
		self.queries, self.qassoc = gtinput.fetch_search_terms(self.infile)
		return self.queries, self.qassoc



	def get_ratio_ba(self, query, date):

		ds = self.gtres[query]['data']['Date']
		if type(self.gtres[query]['data'])!=type(None):
			searches = self.gtres[query]['data'][query]
		else:
			print('Error: requested metric for data that does not exist.')
			exit()
		ibefore = np.where(ds<=date)[0]
		iafter = np.where(ds>date)[0]
		
		return np.sum(searches[ibefore])/np.sum(searches[iafter])


	def plot_tseries(self, qlist, log=True):
		data_list = []
		dates = []
		factors = []

		for query in qlist:
			if type(self.gtres[query]['data'])!=type(None):
				data_list.append(self.gtres[query]['data'][query])
				dates.append(self.gtres[query]['data']['Date'])
				factors.append(self.gtres[query]['factor'])
			else:
				print('Error: requested metric for data that does not exist.')
				exit()
	
		gtplot.tseries(dates, data_list, factors, quer_list=qlist, log=log)


	def main(self):
		self.gtres, self.gtd1, self.gtd2 = gtutils.relative_queryset(self.queries, self.name+'_relqs', self.trange, qassoc=self.qassoc, loc=self.location)
		self.save()


		self.complete = True

		return self.gtres


	def output2csv(self):
		
		gtout.relative_searches_csv(self.gtres, self.qassoc, self.name+'_relative')
		
		gtout.individual_searches_csv(self.gtres, self.qassoc, self.name+'_individual')
		
		return None


	
