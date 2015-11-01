#!/usr/bin/env python                                                                                                                                

## @auth John Allard, Nick Church, others
## @date Oct 2015
## @github https://github.com/jhallard/praxyk
## @license MIT


import os, sys, json, requests
import subprocess, argparse, getpass
import datetime as dt

class PraxykException(Exception):
    def __init__(self, message='', praxyk_instance=None, errors=None):
        super(Exception, self).__init__(message)
        self.errors = errors
