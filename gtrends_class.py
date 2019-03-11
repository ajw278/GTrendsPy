from __future__ import print_function

#Python distribution modules
import os


#The following modules are written for this code:
import saveload as sl
import gtrends_input as gtinput
import gtrends_utilities as gtutils
import gtrends_output as gtout




class gtrends_dataset():
	def __init__(self, name, infile_name, trange, load=True, force_analysis=False):
		
		self.name = name
		self.infile = infile_name
		self.trange = trange
		self.complete =False

		if self.check_previous() and not load:
			print('Previous version found, but load not requested.')
			print('Please remove/rename previous version before continuing')
			exit()
		elif self.check_previous() and load:
			self.load()
		else:
			self.save()
			
		if not self.complete or force_analysis:
			self.get_input()
			self.main()


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


	def main(self):
		self.gtres, self.gtd1, self.gtd2 = gtutils.relative_queryset(self.queries, self.name+'_relqs', self.trange, qassoc=self.qassoc)
		self.save()

		gtout.write_to_csv(self.gtres, self.qassoc, self.name+'_basic')

		self.complete = True

		return self.gtres


	
