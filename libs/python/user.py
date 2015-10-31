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


# @info - This class represents a single Praxyk user and the actions that can be made that are directly
#            related to each user. That means this class can be used to set user info then post that info to
#          create a new user, or you can just set the user_id and auth_token and use the get() function to
#          get all of the rest of the info on a user. Deletion a updates are also supported through put() and
#          update()
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
        response = super(User, self).get(self.USERS_ROUTE+str(self.user_id), payload)
        if response :
            self.user = response['user']
            self.user_id = self.user['user_id']
            self.name = self.user['name']
            self.email = self.user['email']
            self.created_at = self.user['created_at']
            self.active = self.user['active']
            return self.user
        return None

    # @info - create a new user with the user attributes defined as members of this class
    def post(self, password) :
        payload = { 'name' : self.name,
                    'email': self.email,
                    'password' : password}
        response = super(User, self).post(self.USERS_ROUTE, payload)
        if response :
            self.user = response['user']
            self.user_id = self.user['user_id']
            self.name = self.user['name']
            self.email = self.user['email']
            self.created_at = self.user['created_at']
            self.active = self.user['active']
            return self.user
        return None

    def to_dict(self) :
        if self.user_id :
            return {
                    'name' : self.name,
                    'email' : self.email,
                    'active' : self.active,
                    'user_id' : self.user_id,
                    'created_at' : self.created_at
                    }
        else :
            sys.stderr.write("User has not been obtained or constructed yet (i.e. call get() to get the user or push() to create them)\n")
            return {}
    
