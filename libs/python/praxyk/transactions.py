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
from paginated import Paginated
from transaction import Transaction


# @info - This class represents a group of Transactions as returned through the /transactions/ route.
#         This class encapsulates the pagination behavior by exposing functions like next_page(), first_page(),
#         and last_page() that will change the contents of the container of transactions contained inside to fit
#         the appropriate page.
class Transactions(Paginated) :

    def __init__(self, user_id=None, **kwargs) :
        super(Transactions, self).__init__(**kwargs)
        self.transactions = []
        self.transactions_raw = ""
        self.user_id = user_id

    # @info - standard wrapper around the GET /transactions/ route. Takes the standard pagination-related parameters,
    #         if those don't exist it uses the ones defined as member variables for the class.
    def get(self, user_id = None, **kwargs) :
        payload = {'token' : self.auth_token}

        if user_id :
            self.user_id = user_id

        if self.user_id  :
            payload['user_id'] = self.user_id

        try :
            response = super(Transactions, self).get(url=self.TRANSACTIONS_ROUTE, payload=payload, **kwargs)
            if response :
                if response.get('page', None) :
                    self.transactions_raw = response['page'].get('transactions', None)
                else :
                    self.transactions_raw = response.get('transactions', None)
                if not self.transactions_raw : 
                    return None
                for trans in self.transactions_raw :
                    self.transactions.append(Transaction(auth_token=self.auth_token, caller=self.caller, local=self.local, port=self.port,  **trans))
                return self.transactions_raw
        except Exception as e :
            print str(e)
            raise e
        return None


    def to_json(self) :
        tdict = self.to_dict()
        # turn the Transaction object into serializable dictionaries to be jsonified
        tdict['transactions'] = [t.to_dict() for t in tdict['transactions']]
        return json.dumps(tdict)


    def to_dict(self) :
        base_dict = super(Transactions, self).to_dict()
        transaction_dict = {
                'user_id' : self.user_id,
                'transactions' : self.transactions,
                }
        base_dict.update(transaction_dict)
        return base_dict

