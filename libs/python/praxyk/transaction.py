#!/usr/bin/env python

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/praxyk/praxyk-clients
## @license MIT


import os, sys, json, requests, time
import subprocess, argparse, getpass
import datetime as dt
from praxyk_exception import PraxykException
from base import PraxykBase
from results import Results


# @info - This class represents a single Praxyk user and the actions that can be made that are directly
#         related to each user. That means this class can be used to set user info then post that info to
#         create a new user, or you can just set the user_id and auth_token and use the get() function to
#         get all of the rest of the info on a user. Deletion a updates are also supported through put() and
#         update()
class Transaction(PraxykBase) :

    def __init__(self, trans_id=None, name=None, user_id=None, status=None, created_at=None,
                 finished_at=None, command_url=None, service=None, model=None, uploads_total=None,
                 uploads_success=None, uploads_failed=None, size_total_KB=None, **kwargs) :
        super(Transaction, self).__init__(**kwargs)
        self.trans_id = trans_id
        self.name = name
        self.user_id = user_id
        self.status = status
        self.created_at = created_at
        self.finished_at = finished_at
        self.command_url = command_url
        self.service = service
        self.model = model
        self.uploads_total = uploads_total
        self.uploads_success = uploads_success
        self.uploads_failed = uploads_failed
        self.size_total_KB = size_total_KB

    def get(self) :
        if not self.trans_id : return None
        payload = {'token' : self.auth_token}
        try :
            route = self.TRANSACTIONS_ROUTE+str(self.trans_id)
            response = super(Transaction, self).get(route, payload)
            if response :
                self.transaction = response['transaction']
                self.trans_id = self.transaction.get('trans_id', None)
                self.name = self.transaction.get('name', None)
                self.user_id = self.transaction.get('user_id', None)
                self.status = self.transaction.get('status', None)
                self.created_at = self.transaction.get('created_at', None)
                self.finished_at = self.transaction.get('finished_at', None)
                self.command_url = self.transaction.get('command_url', None)
                self.service = self.transaction.get('service', None)
                self.model = self.transaction.get('model', None)
                self.uploads_total = self.transaction.get('uploads_total', None)
                self.uploads_success = self.transaction.get('uploads_success', None)
                self.uploads_failed = self.transaction.get('uploads_failed', None)
                self.size_total_KB = self.transaction.get('size_total_KB', None)
                return self

        except Exception as e:
            raise PraxykException('Error: malformed response from GET request for transaction \'%s\'. Unable to load result dictionary' % self.trans_id)
        return {}


    # @info - wait for the transaction to either finish or fail, sleeps for interval seconds, timesout at timeout seconds
    def spin(self, interval=1, timeout=60) :
        length = 0
        if interval <= 0 : return False
        while self.status in ['active', 'new'] and length <= timeout:
            time.sleep(interval)
            length += interval
            self.get()
        return self.status in ['finished', 'failed']


    # @info - return the results object associated with this transction
    def results(self, *args, **kwargs) :
        return Results(trans_id=self.trans_id, auth_token=self.auth_token, caller=self.caller,
                       local=self.local, port=self.port, *args, **kwargs)

    def put(self, cancel=False):
        if self.trans_id and cancel:
            try:
                payload = {'token' : self.auth_token, 'cancel' : cancel}
                response = super(Transaction, self).put(self.TRANSACTIONS_ROUTE+str(self.trans_id), payload)
                if response:
                    self.transaction = response['transaction']
                    self.trans_id = self.transaction.get('trans_id', None)
                    self.command_url = self.transaction.get('command_url', None)
                    self.data_url = self.transaction.get('data_url', None)
                    self.results_url = self.transaction.get('results_url', None)
                    self.status = self.transaction.get('status', None)
                    self.service = self.transaction.get('service', None)
                    self.model = self.transaction.get('model', None)
                    self.created_at = self.transaction.get('created_at', None)
                    self.uploads_total = self.transaction.get('uploads_total', None)
                    self.uploads_success = self.transaction.get('uploads_success', None)
                    self.uploads_failed = self.transaction.get('uploads_failed', None)
                    self.size_total_KB = self.transaction.get('size_total_KB', None)
                    return self.transaction
            except:
                raise PraxykException('Error with response received from call to \'put\', updating transaction \'%s\'' % self.trans_id)

    def to_dict(self) :
        try:
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
        except Exception as e:
            raise PraxykException('Error converting transaction to dictionary in call to \'to_dict\'', errors=self)
