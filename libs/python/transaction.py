#!/usr/bin/env python                                                                                                                                

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/jhallard/praxyk
## @license MIT


import os, sys, json, requests
import subprocess, argparse, getpass
import datetime as dt

from base import PraxykBase


class Praxyk(PraxykBase) :
    TOKENS_ROUTE = self.BASE_ROUTE + "tokens/"
	USERS_ROUTE = self.BASE_ROUTE + "users/"

    # base headers
    headers = {'content-type': 'application/json'}

    def __init__(self, auth_token="", email="", password="") :
		super(Praxyk, self).__init__(auth_token, email, password)

		if auth_token or (email and password) :
			if not self.login(auth_token=auth_token, email=email, password=password) :
				sys.stderr.write("Could not Log-In, All Requests Will Fail Until You Log-In\n")

	# @info - takes either an existing auth_token or an email and password and logs the user
	# 		  in via the Praxyk api /tokens/ route. Will store the returned user info in
	# 		  member variables that can be stored easily for later.
    def login(self, auth_token="", email="", password="") :
        if auth_token :
            payload = {'token' : self.auth_token}
            results = self.get(TOKENS_ROUTE, payload)
            if results :
                self.user = results['user']
                self.user_id = self.user['user_id']
                self.auth_token = results['token']
                return True
        if email and password :
            payload = {'email' : email, 'password' : password}
            results = self.post(TOKENS_ROUTE, payload)
            if results :
                self.user = results['user']
                self.user_id = self.user['user_id']
                self.auth_token = results['token']
            return False

	# @info - returns information on a specific user, as returned through the /users/X route. If no name
	#		  is given, the user that was logged in during construction is returned. If  a name is given
	#		  that user is grabbed (note only admins can get info on other users)
	@self.requires_auth
	def get_user(self, user_id=None) :
		if user_id=None :
			user_id = self.user_id
		payload = {'token' : self.token}
		response = self.get(USERS_ROUTE+str(user_id), payload)
		return results
		
