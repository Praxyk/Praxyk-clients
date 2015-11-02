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
from transaction import Transaction
from transactions import Transactions


# @info - This class represents a single Praxyk user and the actions that can be made that are directly
#         related to each user. That means this class can be used to set user info then post that info to
#         create a new user, or you can just set the user_id and auth_token and use the get() function to
#         get all of the rest of the info on a user. 
#         Deletions and updates are also supported through put() and delete()
class User(PraxykBase) :

    def __init__(self, name=None, user_id=None, email=None, active=None, created_at=None, **kwargs) :
        super(User, self).__init__(**kwargs)
        self.name = name
        self.user_id = user_id
        self.email = email
        self.created_at = created_at
        self.active = active

    def get_transactions(self) :
        # return Transactions object constructed from user
        pass

    # @info - if the auth token and user id are set, you can call get to fill the rest of the fields
    #         with data from the API
    def get(self) :
        payload = {'token' : self.auth_token}
        try :
            response = super(User, self).get(self.USERS_ROUTE+str(self.user_id), payload)
            if response :
                self.caller = response['user']
                self.user_id = self.caller['user_id']
                self.name = self.caller['name']
                self.email = self.caller['email']
                self.created_at = self.caller['created_at']
                self.active = self.caller['active']
                return self.caller
        except Exception as e :
            sys.stderr.write(str(e))
        return None

    # @info - create a new user with the user attributes defined as members of this class
    def post(self, password) :
        payload = { 'name' : self.name,
                    'email': self.email,
                    'password' : password}
        try :
            response = super(User, self).post(self.USERS_ROUTE, payload)
            if response :
                self.caller = response['user']
                self.user_id = self.caller['user_id']
                self.name = self.caller['name']
                self.email = self.caller['email']
                self.created_at = self.caller['created_at']
                self.active = self.caller['active']
                return self.caller
        except Exception as e :
            sys.stderr.write(str(e))
        return None

	# @info -  This is convenient factory function for generating a Transaction object that is pre-loaded with the
    #          information specific to this user, like the auth_token stored and the user_id associated with this object.
    def transaction(self, *args, **kwargs) :
        return Transaction(auth_token=self.auth_token, caller=self.caller, user_id=self.caller.get('user_id', None),
                           local=self.local, port=self.port, *args, **kwargs)

	# @info -  This is convenient factory function for generating a Transactions object that is pre-loaded with the
    #          information specific to this user, like the auth_token stored and the user_id associated with this object.
    def transactions(self, *args, **kwargs) :
        return Transactions(auth_token=self.auth_token, caller=self.caller, user_id=self.caller.get('user_id', None),
                           local=self.local, port=self.port, *args, **kwargs)

    def to_dict(self) :
        base_dict = super(User, self).to_dict()
        user_dict = {
                    'name' : self.name,
                    'email' : self.email,
                    'active' : self.active,
                    'user_id' : self.user_id,
                    'created_at' : self.created_at
                    }
        base_dict.update(user_dict)
        return base_dict
    
