#!/usr/bin/env python                                                                                                                                

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/jhallard/praxyk
## @license MIT


import os, sys, json, requests
import subprocess, argparse, getpass
import datetime as dt
from praxyk_exception import PraxykException
from paginated import Paginated
from result import Result


# @info - this class represents a grouping of Result classes that correspond to a single transaction.
#         Because the /results/ API route is paginated, this class is also paginated by default. This class
#         is normally constructed via a valid Transaction object, and upon construction from that object this
#         class will be filled with the needed data to page through a transaction's results
class Results(Paginated) :

    def __init__(self, trans_id, *args,  **kwargs) :
        super(Results, self).__init__(*args, **kwargs)
        self.results= []
        self.results_raw = ""
        self.trans_id = trans_id

    # @info - standard wrapper around the GET /results/ route. Takes the standard pagination-related parameters,
    #         if those don't exist it uses the ones defined as member variables for the class.
    def get(self, trans_id = None, **kwargs) :
        payload = {'token' : self.auth_token}

        if trans_id :
            self.trans_id = trans_id

        if self.trans_id  :
            payload['trans_id'] = self.trans_id

        response = super(Results, self).get(url=self.RESULTS_ROUTE+str(self.trans_id), payload=payload, **kwargs)
        if response :
            if response.get('page', None) :
                self.results_raw = response['page'].get('results', None)
            else :
                self.results_raw = response.get('results', None)
            for result in self.results_raw :
                self.results.append(Result(auth_token=self.auth_token, caller=self.caller,
                                           local=self.local, port=self.port, 
                                           trans_id=self.trans_id, user_id=self.caller.get('user_id', None), **result))
            return self
        return None


    def to_json(self) :
        tdict = self.to_dict()
        # turn each Result object into serializable dictionary to be jsonified
        tdict['results'] = [t.to_dict() for t in tdict['results']]
        return json.dumps(tdict)


    def to_dict(self) :
        base_dict = super(Results, self).to_dict()
        results_dict = {
                'trans_id' : self.trans_id,
                'results' : self.results,
                }
        base_dict.update(results_dict)
        return base_dict

