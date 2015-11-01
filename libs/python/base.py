#!/usr/bin/env python                                                                                                                                

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/jhallard/praxyk
## @license MIT


import os, sys, json, requests
import subprocess, argparse, getpass
import datetime as dt
from praxyk_exception import PraxykException

# @info - This is the base class for all other classes in the Praxyk python library.
#         It serves to hold data and functions that are common to all classes of the 
#         library. Examples of this are base url's for routing, pre-set http headers,
#         and functions for return error checking. We also hold user auth info
class PraxykBase(object) :


    # base headers, child classes can add to these
    headers = {'content-type': 'application/json'}

    def __init__(self, auth_token="", user=None, local=False, port=5000, **kwargs) :
        self.auth_token = auth_token
        self.caller = user # the dictionary containing all of the user's information 
                           # (user as in caller, owner of the auth token)
        self.local = local
        self.port  = port

        self.BASE_URL = ("http://127.0.0.1:" + str(self.port) + "/") if self.local else "http://api.praxyk.com/"
        self.VERSION  = "v1/"
        self.BASE_ROUTE         = self.BASE_URL + self.VERSION
        self.TOKENS_ROUTE       = self.BASE_ROUTE + "tokens/"
        self.USERS_ROUTE        = self.BASE_ROUTE + "users/"
        self.TRANSACTIONS_ROUTE = self.BASE_ROUTE + "transactions/"


    # @info - simple helper wrapper function that can be used to ensure a function
    #           is only called if the self.auth_token is not Null, if it is this function
    #          will print a simple error message letting the user know
    @staticmethod
    def requires_auth(f):
        @wraps(f)                                                                                                                                        
        def decorated(*args, **kwargs):
            if not self.auth_token :
                raise PraxykException(message="An auth token is required to call this function. Please login and try again.\n")
                return False
            return f(*args, **kwargs)
        return decorated

    # @info - takes the dictionary returned by self.to_dict and jsonifies it.
    def to_json(self) :
        return json.dumps(self.to_dict())

    # @info - child classes should override this to return a dictionary containing the
    #         relevant members and their values. AKA User.to_dict() should return 
    #         {name : 'first last', email : 'who@areyou.com', token : 'lksjdlfkjsl;dkjfl;sajkd' ...}
    def to_dict(self) :
        return {
            'auth_token':self.auth_token,
            'user':self.user,
        }


    # @info - looks at the raw response and prints relevant error messages if necessary
    def check_return(self, r) :
        if not r or not r.text :
            if "404" in r.text :
                raise PraxykException(message="404 : Content Not Found.")
            elif "403" in r.text :
                raise PraxykException(message="403 : Unauthorized Request.")
            elif "400" in r.text :
                raise PraxykException(message="400 : Bad Request.")
            elif "500" in r.text :
                raise PraxykException(message="500 : System Error (if you think this is a bug please tell the Praxyk team! (github.com/praxyk)")
            else :
                raise PraxykException(message="Request Could not be Fufilled.\nDetails : %s\n"%r.text)
            return None
        else :
            return r

    def get(self, url, payload) :
        r = requests.get(url, data=json.dumps(payload), headers=self.headers)
        if not self.check_return(r) :
            raise PraxykException(message="Request Failed (GET) : Url (%s) | Payload (%s)" % (url, payload))
        return json.loads(r.text)

    def post(self, url, payload) :
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        if not self.check_return(r) :
            raise PraxykException(message="Request Failed (POST) : Url (%s) | Payload (%s)" % (url, payload))
        return json.loads(r.text)

    def put(self, url, payload) :
        r = requests.put(url, data=json.dumps(payload), headers=self.headers)
        if not self.check_return(r) :
            raise PraxykException("Request Failed (PUT) : Url (%s) | Payload (%s)" % (url, payload))
        return json.loads(r.text)

    def delete(self, url, payload) :
        r = requests.delete(url, data=json.dumps(payload), headers=self.headers)
        if not self.check_return(r) :
            raise PraxykException("Request Failed (DELETE) : Url (%s) | Payload (%s)" % (url, payload))
        return json.loads(r.text)
