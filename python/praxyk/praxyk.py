#!/usr/bin/env python

## @auth John Allard, Nick Church
## @date Oct 2015
## @github https://github.com/jhallard/praxyk
## @license MIT

#import praxyk_results
#import praxyk_transaction
#import praxyk_user
import requests
import sys, os
import argparse
import json

PRAXYK_WEBSITE = 'http://api.praxyk.com'

class PraxykException(Exception):
	def __init__(self, message='', praxyk_instance=None, errors=None):
		super(Exception, self).__init__()
		self.errors = errors


def login(username=None, password=None):
	if username and password:
		try:
			return requests.get('%s/users/' % PRAXYK_WEBSITE, auth=(username, password))
		except Exception as e:
			print 'Error verifying login credentials'
			return
	else:
		print 'Username or password missing, only one supplied'


class Praxyk:
	class PraxykUser:
		def __init__(self, username=None, password=None, authok=None):
			if username and password:
				self.username = username
				self.password = password
				#attempt login, if it fails auth, raise an exception
				print 'response ', response
				raise PraxykException(message='Could not confirm user authorization with given username/password combo or authorization token', praxyk_instance=self)
			elif authtok:
				self.authtok = authtok
				# attempt login
				# if not authorized:
				raise PraxykException(message='Could not confirm user authorization with given username and password or authorization token', praxyk_instance=self)
			else:
				raise PraxykException(message='No username and password or authorization token present.\nIf you do not have a valid username and password or authorization token, refer to: %s\n' % PRAXYK_WEBSITE, praxyk_instance=self)
		def get():

		def update()
	def __init__():

