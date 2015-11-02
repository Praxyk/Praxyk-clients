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

    def __init__(self, pagination=None, first_page_num=None, last_page_num=None, 
                 prev_page_num=None, next_page_num=None, page_size=None, **kwargs) :
        
        super(Paginated, self).__init__(**kwargs)
        self.next_page_num = next_page_num
        self.prev_page_num = prev_page_num
        self.last_page_num = last_page_num
        self.first_page_num = first_page_num
        self.page_size = page_size
        self.pagination = pagination



    # @info - child classes should call this first (via super()), then add their own key/vals 
    #         to the dictionary returned and return that to the user. See praxyk.User for ex.
    def to_dict(self) :
        return {
            'auth_token':self.auth_token,
            'caller':self.caller,
        }

