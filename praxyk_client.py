#!/usr/bin/python
import requests
import sys, os
import argparse
import datetime
import json
import getpass
import subprocess
import ConfigParser
import praxyk

from os.path import expanduser

global CONFIG_DIR 
global CLIENT_CONFIG_FILE
global USER_EMAIL
global USER_PASS

CONFIG_DIR = str(expanduser("~"))+'/.praxyk_client/'
CLIENT_CONFIG_FILE = CONFIG_DIR + 'config'


BASE_URL = 'http://127.0.0.1:5000/'
# BASE_URL = 'http://api.praxyk.com:5000/'

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

def load_user():
    config = ConfigParser.ConfigParser()
    try:
        configfile = open(CLIENT_CONFIG_FILE, 'r')
        config.readfp(configfile)
        USER_EMAIL = config.get('defaut', 'email')
        USER_PASS = config.get('default', 'password')
    except Exception:
        sys.stderr.write('Unable to open the local configuration file.')
        return login_user()



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
def login_user(argv=None) :

def register_user() :

def exit_session() :



def change_password(user=None) :

def change_email(user=None) :

def register_user(argv=None) :

def update_user(argv=None) :

def get_user(argv=None) :

def get_users(argv=None) :

GREETING = 'Welcome to the Praxyk command line client!\nPlease enter a command. (help displays a list of commands)\n'

ACTION_MAP = { 'login'  : { ""  : login_user },
            'register'  : { ""  : register_user },
            'exit'      : { ""  : exit_session },
            'switch'    : { "user" : switch_user },
            'change'    : {
                            "email" : change_email,
                         "password" : change_password },
            'apply'      : {
                            "coupon": apply_coupon },
            'begin'      : {
                       "transaction": begin_transaction },
            'cancel'     : {
                      "transaction" : cancel_transaction },
            'display'    : { "user" : display_user,
                     "transactions" : display_transactions,
                      "transaction" : display_transaction,
                          "results" : display_results,
                           "result" : display_result,
                            "users" : get_users } }

# @info - main function, loops to get user input and calls
# appropriate functions as per the user's command
if __name__ == "__main__" :
    args = parse_args(sys.argv)
    if args.root :
        CLIENT_CONFIG_FILE = CONFIG_DIR + 'root.config'
    user = load_user(CLIENT_CONFIG_FILE)
    print GREETING
    command = get_input()
    while (command != 'exit'):
        action_func = ACTION_MAP.get(args.action).get(args.noun, None)
        if not action_func :
            sys.stderr.write(('It looks like your input of [%s] is invalid or unimplemented.' % (args.action+" " +args.noun)) 
        action_func(argv=args.specifics)
        command = get_input()

    exit_session()
    
    

