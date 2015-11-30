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
                 item_name=None, item_number=None, size_KB=None, prediction=None, *args, **kwargs) :
        super(Result, self).__init__(*args, **kwargs)
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
        payload = {'token' : self.auth_token, 'page_size' : 1, 'page' : self.item_number}
        try :
            response = super(Result, self).get(self.RESULTS_ROUTE+str(self.trans_id), payload)
            if response :
                page = response['page']
                self.result = page.get('results', [])
                if self.result and len(self.result) >= 1 :
                    self.result = self.result[0]
                    self.status = self.result.get('status', None)
                    self.created_at = self.result.get('created_at', None)
                    self.finished_at = self.result.get('finished_at', None)
                    self.size_KB = self.result.get('size_KB', None)
                    self.item_name = self.result.get('item_name', None)
                    self.item_number = self.result.get('item_number', None)
                    self.prediction = self.result.get('prediction', None)
                    return self
        except Exception, e :
            sys.stderr.write(str(e))
            raise e
        return None


    def to_dict(self) :
        base_dict = super(Result, self).to_dict()
        result_dict = {
                'status' : self.status,
                'trans_id' : self.trans_id,
                'user_id' : self.user_id,
                'created_at' : self.created_at,
                'finished_at' : self.finished_at,
                'size_KB' : self.size_KB,
                'item_name' : self.item_name,
                'item_number' : self.item_number,
                'prediction' : self.prediction
                }
        base_dict.update(result_dict)
        return base_dict

