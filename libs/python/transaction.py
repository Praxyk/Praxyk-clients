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
class Transaction(PraxykBase) :

    def __init__(self, trans_id=None, name=None, user_id=None, status=None, created_at=None, finished_at=None,
                 command_url=None, service=None, model=None, uploads_total=None, uploads_success=None,
                 uploads_failed=None, size_total_kb=None, **kwargs)
        super(Transaction, self).__init__(**kwargs)
        self.name = name
        self.user_id = user_id
        self.created_at = created_at
        self.finished = created_at
        self.status = status

    def get(self) :
        payload = {'token' : self.auth_token}
        response = super(Transaction, self).get(self.TRANSACTIONS_ROUTE+str(self.trans_id), payload)
        if response :
            self.user = response['user']
            self.transaction = response['transaction']
            return self.user
        return None


    def to_dict(self) :
        base_dict = super(self).to_dict()
        transaction_dict = {
                'name' : self.name,
                'status' : self.status,
                'trans_id' : self.trans_id,
                'user_id' : self.user_id,
                'created_at' : self.created_at,
                'finished_at' : self.finished_at,
                'command_url' : self.command_url,
                'service' : self.service,
                'model' : self.model,
                'uploads_total' : self.uploads_total,
                'uploads_success' : self.uploads_success,
                'uploads_faile' : self.uploads_failed,
                'size_total_KB' : self.size_total_KB,
                }
        return base_dict.update(transaction_dict)
    


    def to_json(self) :
        return json.dumps(self.to_dict())
    


