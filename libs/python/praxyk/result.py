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


# @info - This class represents a single result from a request to a Praxyk service. It encapsulates a group
#         of meta-data about the result and the actual prediction data that is returned from the service that
#         the request was made to. Read the API docs for more info on Results.
class Result(PraxykBase) :

    def __init__(self, trans_id=None, user_id=None, status=None, created_at=None, finished_at=None,
                 item_name=None, item_number=None, size_KB=None, prediction=None)
        super(Result, self).__init__(**kwargs)
        self.trans_id = trans_id
        self.user_id = user_id
        self.status = status
        self.created_at = created_at
        self.finished_at = finished_at
        self.size_KB = size_KB
        self.item_name = item_name
        self.item_number = item_number,
        self.prediction = prediction

    def get(self) :
        payload = {'token' : self.auth_token}
        try :
            response = super(Result, self).get(self.RESULTS_ROUTE+str(self.trans_id), payload)
            if response :
                self.result 
                self.trans_id = trans_id
                self.user_id = user_id
                self.status = status
                self.created_at = created_at
                self.finished_at = finished_at
                self.size_KB = size_KB
                self.item_name = item_name
                self.item_number = item_number,
                self.prediction = prediction
                return self.transaction
        except Exception, e :
            sys.stderr.write(str(e))
        return None


    def to_dict(self) :
        base_dict = super(Transaction, self).to_dict()
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
                'uploads_failed' : self.uploads_failed,
                'size_total_KB' : self.size_total_KB,
                }
        base_dict.update(transaction_dict)
        return base_dict

