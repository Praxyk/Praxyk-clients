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


# @info - This class represents a group of Transactions as returned through the /transactions/ route.
#         This class encapsulates the pagination behavior by exposing functions like next_page(), first_page(),
#         and last_page() that will change the contents of the container of transactions contained inside to fit
#         the appropriate page.
class Transactions(PraxykBase) :

    def __init__(self, user_id=None, pagination=None, page_size=None, page=None, **kwargs) :
        super(Transactions, self).__init__(**kwargs)
        self.transactions = []
        self.transactions_raw = ""
        self.next_page_num = None
        self.prev_page_num = None
        self.last_page_num = None
        self.first_page_num = None
        self.page_size = page_size
        self.page = page
        self.pagination = pagination
        self.user_id = user_id

    # @info - standard wrapper around the GET /transactions/ route. Takes the standard pagination-related parameters,
    #         if those don't exist it uses the ones defined as member variables for the class.
    def get(self, user_id = None, pagination=None, page_size=None, page=None) :
        payload = {'token' : self.auth_token}

        if user_id    : self.user_id = user_id
        if pagination : self.pagination = pagination
        if page_size  : self.page_size = page_size
        if page       : self.page = page

        if self.user_id    : payload['user_id'] = self.user_id
        if self.page_size  : payload['page_size'] = self.page_size
        if self.page       : payload['page'] = self.page
        if self.pagination : payload['pagination'] = self.pagination

        try :
            response = super(Transactions, self).get(self.TRANSACTIONS_ROUTE, payload)
            if response :
                if response.get('page', None) :
                    self.transactions_raw = response['page'].get('transactions', None)
                else :
                    self.transactions_raw = response.get('transactions', None)
                if not self.transactions_raw : return None
                self.transactions = [Transaction(auth_token=self.auth_token, caller=self.caller, **trans) for trans in self.transactions_raw]
                self.next_page_num = self.get_params_from_url(response.get('next_page', "")).get('page', None)
                self.prev_page_num = self.get_params_from_url(response.get('prev_page', "")).get('page', None)
                self.first_page_num = self.get_params_from_url(response.get('first_page', "")).get('page', None)
                self.last_page_num = self.get_params_from_url(response.get('last_page', "")).get('page', None)

                self.next_page_num = int(self.next_page_num[0]) if self.next_page_num else None
                self.prev_page_num = int(self.prev_page_num[0]) if self.prev_page_num else None
                self.first_page_num = int(self.first_page_num[0]) if self.first_page_num else None
                self.last_page_num = int(self.last_page_num[0]) if self.last_page_num else None
                self.page = response.get('page', {}).get('page_number', None)
                return self.transactions_raw
        except Exception as e :
            sys.stderr.write(str(e))
        return None


    # @info - these next four functions can be used after a page of results has already been obtained via the get function.
    #         When that function is called, the results returned contain links to the next page, prev page, first page,
    #         and last page of the transactions. We store those page numbers and make them accessable via these functions, ex:
    #         tr = Transactions(user_id=45, auth_token=XXXX); tr.get(); trans_1 = tr.transactions; tr.next_page(); trans_2 = tr.transactions
    def next_page(self) :
        payload = {'token' : self.auth_token}
        try :
            if self.next_page_num:
                self.page = int(self.next_page_num)
                self.pagination = True
                return self.get()
        except Exception as e :
            sys.stderr.write(str(e))
        return None

    def prev_page(self) :
        payload = {'token' : self.auth_token}
        try :
            if self.prev_page_num:
                self.page = int(self.prev_page_num)
                self.pagination = True
                return self.get()
        except Exception as e :
            sys.stderr.write(str(e))
        return None

    def last_page(self) :
        payload = {'token' : self.auth_token}
        try :
            if self.last_page_num:
                self.page = int(self.last_page_num)
                self.pagination = True
                return self.get()
        except Exception as e :
            sys.stderr.write(str(e))
        return None

    def first_page(self) :
        payload = {'token' : self.auth_token}
        try :
            if self.first_page_num :
                self.page = int(self.first_page_num)
                self.pagination = True
                return self.get()
        except Exception as e :
            sys.stderr.write(str(e))
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
                'page' : self.page,
                'pagination' : self.pagination,
                'page_size' : self.page_size,
                'next_page' : self.next_page_num,
                'prev_page' : self.prev_page_num,
                'last_page' : self.last_page_num,
                'first_page' : self.first_page_num
                }
        base_dict.update(transaction_dict)
        return base_dict

