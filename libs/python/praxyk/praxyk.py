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
from user import User
from transaction import Transaction
from transactions import Transactions
from result import Result
from results import Results

from pod import pod_ocr, pod_face_detect


# @info - Main Praxyk class for the API. This class is used to manage one's account and perform
#         most data-grabbing operations. User's log in through this class (either in the constructor
#         or the login function), then can call the various get_* functions like get_user to get info
#         on their account. To actually create users,`
class Praxyk(PraxykBase) :

    def __init__(self, login=True, email=None, password=None, *args, **kwargs)  :
        super(Praxyk, self).__init__(*args, **kwargs)

        # if they gave the login flag and credentials, go ahead and login
        # note that self.login throws an exception upon failure so this will propogate
        # the exception out of the constructor
        if login and (self.auth_token or (email and password)) :
            self.login(auth_token=self.auth_token, email=email, password=password)

    # @info - takes either an existing auth_token or an email and password and logs the user
    #          in via the Praxyk api /tokens/ route. Will store the returned user info in
    #          member variables that can be stored easily for later.
    def login(self, auth_token=None, email="", password="") :
        results = {}
        if auth_token :
            payload = {'token' : auth_token}
            results = super(Praxyk, self).get(self.TOKENS_ROUTE, payload)
        elif email and password :
            payload = {'email' : email, 'password' : password}
            results = super(Praxyk, self).post(self.TOKENS_ROUTE, payload)
        else :
            return False

        if results :
            self.caller = results.get('user', None)
            self.auth_token = results.get('token', None)
            return True
        else :
            raise PraxykException(message="Could not Log-In")
        return False

    # @info - returns a praxyk.User object that will pre-contain the authorization key and routing
    #         info associated with this object. So instead of having to say user=praxyk.User(auth_token=xxx, ...),
    #         they can just say pr = Praxyk(email=xxx, password=yyy);user = pr.User();user.get(); print user.to_json()
    def user(self, *args, **kwargs) :
        return User(auth_token=self.auth_token, caller=self.caller, user_id=None if not self.caller else self.caller.get('user_id', None),
                    local=self.local, port=self.port, *args, **kwargs)

    # @info - like the User function, this is a convenient factory class to instantiate a Transaction object with
    #         the base attributes (auth_token, user_id, port, routes, etc) pre-set with the values from this
    #         existing object.
    def transaction(self, *args, **kwargs) :
        return Transaction(auth_token=self.auth_token, caller=self.caller, local=self.local, port=self.port, *args, **kwargs)

    # @info -  This is convenient factory function for generating a Transactions object that is pre-loaded with the
    #          information specific to this user, like the auth_token stored and the user_id associated with this object.
    def transactions(self, *args, **kwargs) :
        return Transactions(auth_token=self.auth_token, caller=self.caller, local=self.local, port=self.port, *args, **kwargs)

    def result(self, *args, **kwargs) :
        return Result(auth_token=self.auth_token, user_id=None if not self.caller else self.caller.get('user_id', None), caller=self.caller, local=self.local, port=self.port, *args, **kwargs)

    def results(self, *args, **kwargs) :
        return Result(auth_token=self.auth_token, user_id=None if not self.caller else self.caller.get('user_id', None), caller=self.caller, local=self.local, port=self.port, *args, **kwargs)

    def pod(self, service, *args, **kwargs) :
        if service.lower() == 'ocr' :
            return pod_ocr.POD_OCR(auth_token=self.auth_token, caller=self.caller, local=self.local, port=self.port, *args, **kwargs)
        if service.lower() == 'face_detect' :
            return pod_face_detect.POD_FaceDetect(auth_token=self.auth_token, caller=self.caller, local=self.local, port=self.port, *args, **kwargs)
        return None
