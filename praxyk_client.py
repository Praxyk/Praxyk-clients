#!/usr/bin/python
import requests
import sys, os
import argparse
import datetime
import json
import getpass
import subprocess
import praxyk

from os.path import expanduser

global CONFIG_DIR 
global CLIENT_CONFIG_FILE

CONFIG_DIR = str(expanduser("~"))+'/.praxyk_client/'
CLIENT_CONFIG_FILE = CONFIG_DIR + 'config'

ACTIONS = ['login', 'register', 'create', 'update', 'get', 'exit']
NOUNS = ['transaction', 'transactions', 'result', 'results', 'user', 'users']


BASE_URL = 'http://127.0.0.1:5000/'
# BASE_URL = 'http://api.praxyk.com:5000/'
TOKENS_URL =  BASE_URL+'tokens/'
COMPUTE_URL = BASE_URL+'compute/'
SNAPSHOTS_URL = BASE_URL+'snapshots/'
USERS_URL = BASE_URL+'users/'
SSHKEYS_URL = BASE_URL+'sshkeys/'

DESCRIPTION = """
Documentation for this script is available here: https://github.com/Praxyk/Praxyk-Clients/wiki/Command-Line-Utility
"""

# @info - parse command line args into useable dictionary
#         right now we only take a config file as an argument
def parse_args(argv) :
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--root', action='store_true',  help="This flag will cause the program to look for a different config file, one that contains " +\
                                       "a root token. If you don't have the root token, giving this flag will only cause everything to fail.")                                                       "depending on what you are doing")
    return parser.parse_args()

def get_input(desc, default=None) :
    desc = desc + ("" if not default else " default : (%s)" % str(default))
    print desc
    inp = sys.stdin.readline().strip()
    inp = inp if inp else default
    while not inp :
        inp = sys.stdin.readline().strip()
    return inp

def get_passwd(desc = None) :
    inp = ""
    while not inp :
        inp = getpass.getpass(desc).strip()
    return inp

def get_input_choices(desc, choices) :
    print desc + " : "
    # print "Select One of the Following (by number) : "
    count = 1
    for x in choices :
        print str(count) + ".)  " + str(x)
        count += 1

    inp = None 
    while not inp or not inp.isdigit() or (int(inp) <= 0 or int(inp) > len(choices)) :
        inp = sys.stdin.readline().strip()
        if not inp or not inp.isdigit() or (int(inp) <= 0 or int(inp) > len(choices)) :
            print "Incorrect Choice. Select Again."
    
    return int(inp)-1

# @info - gets a yes/no input from the user, returns true if user chose yes
#         else returns false
def get_yes_no(desc) :
    inp = ""
    print desc + " (Y/n)"
    while inp not in ['y', 'Y', 'n', 'N', 'yes', 'Yes', 'No', 'no'] :
        inp = sys.stdin.readline().strip()

    return inp in ['y', 'Y', 'yes', 'Yes']

# @info - looks at the raw response and prints relevant error messages if necessary
def check_return(r) :
    if not r or not r.text :
        if "404" in r.text :
            sys.stderr.write("Content Not Found. Double check all content-IDs are correct (username, instance id, etc).\n")
        elif "401" in r.text :
            sys.stderr.write("Request Could not be Authorized. If you haven't logged in today, do so. If error persists, contact John.\n")
        elif "500" in r.text :
            sys.stderr.write("The Server had a Hiccup, do you mind forwarding this stack trace to John?\n")
            sys.stderr.write(str(80*'-'+'\n'+r.text+80*'-'+'\n'))
        else :
            sys.stderr.write("Request Could not be Fufilled.\nDetails : %s\n"%r.text)
        return False
    else :
        return True


# @info - grabs the user's current token and username from a local file and return it to be used.
def load_auth_info() :
    if not os.path.isfile(CLIENT_CONFIG_FILE) :
        return {}
    with open(CLIENT_CONFIG_FILE) as fh :
        config_data = json.load(fh)
        return config_data
    return {}

# @info - this logs the user into the API service by submitting their username and password in return for a temporary access
#         token. This token is stored in a hidden directory and can be loaded automatically when the user makes future requests.
def login_user() :

def change_password(user=None) :

def change_email(user=None) :

def register_user(argv=None) :

def update_user(argv=None) :

def get_user(argv=None) :

def get_users(argv=None) :

ACTION_MAP = {  'login'      	: { ""  : login_user }
		'register'   	: { ""	: register_user }
		'exit'		: { ""	: exit_session }
		'switch'        : { "user" : switch_user }
		'change'        : { "email": change_email,
		                 "password": change_password }
		'apply'         : {"coupon": apply_coupon }
		'begin'         : {"transaction": begin_transaction }
		'cancel'        : {"transaction": cancel_transaction }
                'display'    	: { "user" : display_user,
                            "transactions" : display_transactions,
                             "transaction" : display_transaction,
                                 "results" : display_results,
                                  "result" : display_result,
                                   "users" : get_users }
}

# @info - main function, has the sys.argv args parsed and performs a switch based on those arguments.
if __name__ == "__main__" :
    args = parse_args(sys.argv)

    if args.root :
        CLIENT_CONFIG_FILE = CONFIG_DIR + 'root.config'

    action_func = ACTION_MAP.get(args.action).get(args.noun, None)
    if not action_func :
        sys.stderr.write(("It looks like your input of [%s] is invalid or unimplemented." +\
                         " If you think this is wrong tell John. \n") % (args.action+" " +args.noun)) 
        sys.exit(1)
    res = action_func(argv=args.specifics)
    
    sys.exit(0 if res else 1)
    
    

