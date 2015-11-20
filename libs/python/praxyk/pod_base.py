#!/usr/bin/env python                                                                                                                                

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/praxyk/praxyk-clients
## @license MIT


import os, sys, json, requests
import subprocess, argparse, getpass
import datetime as dt
from praxyk_exception import PraxykException
from base import PraxykBase
from results import Results
from transaction import Transaction


# @info - This represents a base class that all pod models can derive from. This class will hold
#          the meta-data common to all types of pod transactions, like user id, creation time, status,
#          etc.
class PODBase(PraxykBase) :

    def __init__(self, name=None, user_id=None, *args, **kwargs) :
        super(PODBase, self).__init__(**kwargs)
        self.name = name


    def post(self, url, payload, files=None, name=None) :
        if name : self.name = name
        if self.name : payload['name'] = self.name

        try :
            response = super(PODBase, self).post(url, payload, files=files)
            if response :
                self.transaction = Transaction(auth_token = self.auth_token,
                                               caller = self.caller, local=self.local,
                                               port=self.port, **response.get('transaction', {}))
                return self.transaction
            return None
        except Exception as e :
            raise e 
        return None


    def to_dict(self) :
        try:
            base_dict = super(Transaction, self).to_dict()
            updated = { "name" : self.name }
            base_dict.update(updated)
            return base_dict
        except Exception as e:
            raise PraxykException('Error converting transaction to dictionary in call to \'to_dict\'', errors=self)
