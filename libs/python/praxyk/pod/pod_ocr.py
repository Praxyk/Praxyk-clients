#!/usr/bin/env python																																

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/jhallard/praxyk
## @license MIT


import os, sys, json, requests
import subprocess, argparse, getpass
import datetime as dt
from praxyk_exception import PraxykException
from base import PraxykBase
from pod_base import PODBase
from results import Results


# @info - This class represents a single Praxyk user and the actions that can be made that are directly
#		 related to each user. That means this class can be used to set user info then post that info to
#		 create a new user, or you can just set the user_id and auth_token and use the get() function to
#		 get all of the rest of the info on a user. Deletion a updates are also supported through put() and
#		 update()
class POD_OCR(PODBase) :

	def __init__(self, file_names=[], *args, **kwargs) :
		super(POD_OCR, self).__init__(*args, **kwargs)
		self.file_names = file_names
		self.transaction = None

	def post(self, file_names=None, **kwargs) :
		if file_names :
			self.file_names = file_names

		files = {}

		try :
			files = []
			for name in self.file_names :
				file_struct = self.load_file(name)
				files.append(file_struct)

			payload = {'token' : self.auth_token}

			# PODBase super class automatically turns the result from the API into a praxyk.Transaction
			# object for us to use
			new_trans = super(POD_OCR, self).post(self.POD_OCR_ROUTE, payload, files=files, **kwargs)
			if new_trans :	
				self.transaction = new_trans
				return self.transaction
			return None
		except Exception as e : 
			raise e
		return None


	def load_file(self, fn) :
		return ('files', (open(fn, 'rb')))

	def to_dict(self) :
		try:
			base_dict = super(Transaction, self).to_dict()
			updated = { "file_names " : self.file_names }
			base_dict.update(updated)
			return base_dict
		except Exception as e:
			raise PraxykException('Error converting transaction to dictionary in call to \'to_dict\'', errors=self)
