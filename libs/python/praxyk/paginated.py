#!/usr/bin/env python                                                                                                                                

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/jhallard/praxyk
## @license MIT


import os, sys, json, requests
import subprocess, argparse, getpass, urlparse
import datetime as dt
from praxyk_exception import PraxykException
from base import PraxykBase

# @info - This is the base class for all other classes in the Praxyk python library.
#         It serves to hold data and functions that are common to all classes of the 
#         library. Examples of this are base url's for routing, pre-set http headers,
#         and functions for return error checking. We also hold user auth info
class Paginated(PraxykBase) :

    def __init__(self, pagination=None, first_page_num=None, last_page_num=None, page=None,
                 prev_page_num=None, next_page_num=None, page_size=None, *args, **kwargs) :
        
        super(Paginated, self).__init__(*args, **kwargs)
        self.next_page_num = next_page_num
        self.prev_page_num = prev_page_num
        self.last_page_num = last_page_num
        self.first_page_num = first_page_num
        self.page_size = page_size
        self.pagination = pagination
        self.page = page


    def get(self, url, payload, pagination=None, page_size=None, page=None) :

        if pagination is not None :
            self.pagination = pagination
        if page_size : 
            self.page_size = page_size
        if page : 
            self.page = page

        if self.page_size is not None  :
             payload['page_size'] = self.page_size
        if self.page is not None :
             payload['page'] = self.page
        if self.pagination is not None :
             payload['pagination'] = self.pagination
        try :
            response = super(Paginated, self).get(url, payload)  
            if response :
                self.next_page_num = self.get_params_from_url(response.get('next_page', "")).get('page', None)
                self.prev_page_num = self.get_params_from_url(response.get('prev_page', "")).get('page', None)
                self.first_page_num = self.get_params_from_url(response.get('first_page', "")).get('page', None)
                self.last_page_num = self.get_params_from_url(response.get('last_page', "")).get('page', None)

                self.next_page_num = int(self.next_page_num[0]) if self.next_page_num else None
                self.prev_page_num = int(self.prev_page_num[0]) if self.prev_page_num else None
                self.first_page_num = int(self.first_page_num[0]) if self.first_page_num else None
                self.last_page_num = int(self.last_page_num[0]) if self.last_page_num else None
                self.page = response.get('page', {}).get('page_number', page)
                
                return response
        except Exception as e :
            print str(e)
            raise PraxykException(message="GET Request Failed in Paginated Class. URL (%s)" % url)
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


    def to_dict(self) :
        base_dict = super(Paginated, self).to_dict()
        updated  = {
                'page' : self.page,
                'pagination' : self.pagination,
                'page_size' : self.page_size,
                'next_page' : self.next_page_num,
                'prev_page' : self.prev_page_num,
                'last_page' : self.last_page_num,
                'first_page' : self.first_page_num
                }
        base_dict.update(updated)
        return base_dict


