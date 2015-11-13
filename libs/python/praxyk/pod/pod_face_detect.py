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
from pod_base import PODBase
from results import Results


class POD_FaceDetect(PODBase) :

    def __init__(self, file_names=[], *args, **kwargs) :
        super(POD_FaceDetect, self).__init__(*args, **kwargs)
        self.file_names = file_names
        self.transaction = None

    def post(self, file_names=None, **kwargs) :
        if file_names :
            self.file_names = file_names

        files = {}

        try :
            files = []
            for name in self.file_names :
                file_struct = self.load_file(name)
                files.append(file_struct)

            payload = {'token' : self.auth_token}

            # PODBase super class automatically turns the result from the API into a praxyk.Transaction
            # object for us to use
            new_trans = super(POD_FaceDetect, self).post(self.POD_FACE_DETECT_ROUTE, payload, files=files, **kwargs)
            if new_trans :    
                self.transaction = new_trans
                return self.transaction
            return None
        except Exception as e : 
            raise e
        return None


    def load_file(self, fn) :
        return ('files', (open(fn, 'rb')))

    def to_dict(self) :
        try:
            base_dict = super(Transaction, self).to_dict()
            updated = { "file_names " : self.file_names }
            base_dict.update(updated)
            return base_dict
        except Exception as e:
            raise PraxykException('Error converting transaction to dictionary in call to \'to_dict\'', errors=self)
