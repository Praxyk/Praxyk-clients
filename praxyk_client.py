#!/usr/bin/python
import requests
import sys, os
import argparse
import datetime
import json
import getpass
import subprocess
import ConfigParser
import traceback
import pdb
from libs.python.praxyk import Praxyk

from os.path import expanduser

global CONFIG_DIR
global CLIENT_CONFIG_FILE
global USER_AUTH
global USER_EMAIL
global USER_PASS
global PRAXYK
global USER
global SCRIPTING

CONFIG_DIR = str(expanduser("~"))+'/.praxyk_client/'
CLIENT_CONFIG_FILE = CONFIG_DIR + 'config'
PROMPT = '=> '
GREETING = '\nWelcome to the Praxyk command line client!\nPlease enter a command. (help displays a list of commands)\n'+\
    'Type ^C at any time to quit.'

#BASE_URL = 'http://127.0.0.1:5000/'
BASE_URL = 'http://api.praxyk.com'

DESCRIPTION = """
Documentation for this script is available here: https://github.com/Praxyk/Praxyk-Clients/wiki/Command-Line-Utility
"""

def set_up_env() :
    if not os.path.exists(CONFIG_DIR) :
        os.makedirs(CONFIG_DIR)

# @info - parse command line args into useable dictionary
#         right now we only take a config file as an argument
def parse_args(argv) :
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--root', action='store_true',  help="This flag will cause the program to look for a different" +\
        " config file, one that contains a root token. If you don't have the root token, giving this flag will only " +\
        "cause everything to fail, depending on what you are doing")
    parser.add_argument('--script', action='store_true', help='This flag will tell the client script that you want to run ' +\
        'it in \'scripting\' mode, where this program will expect only commands to come from the standard input, so as not to ' +\
        'present the script with choices.')
    return parser.parse_args()



def get_input(desc, default=None) :
    if desc == '' :
        desc = PROMPT
    desc = desc + ("" if not default else " default : (%s)" % str(default))
    inp = raw_input(desc).strip()
    inp = inp if inp else default
    while not inp :
        inp = raw_input(desc).strip()
    return inp

def get_passwd(desc = None) :
    if desc:
        print desc
    inp = ""
    while not inp :
        inp = getpass.getpass().strip()
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

# @info - this attempts to load the user's login info from a local config file, or allows them to login/register
#         if such a file does not exist.
def load_user() :
    answer = True
    if not SCRIPTING:
        if not os.path.isfile(CLIENT_CONFIG_FILE):
            answer = get_yes_no('Welcome to the Praxyk client script, we couldn\'t detect a configuration file, ' +\
            'do you have a Praxyk account already?')
            if not answer:
                print 'No problem, we will have you up and running in no time!'
                register_user()
            else:
                return login_user()
        else:
            answer = get_yes_no('Would you like to load user data from the Praxyk config file?')

    if answer or SCRIPTING:
        try:
            config = ConfigParser.ConfigParser()
            configfile = open(CLIENT_CONFIG_FILE, 'r')
            config.readfp(configfile)
            USER_AUTH = config.get('default_section', 'auth_tok')
            if not PRAXYK.login(auth_token=USER_AUTH): # @TODO add support for changing the config section to load
                print 'Unable to log in using the default credentials in config file, please log in with fresh credentials, '+\
                    'or type ^C to exit.'
                return login_user()
            else :
                print 'Successfully logged in using credentials from config file.'
        except Exception:
            sys.stderr.write('Unable to open the local configuration file.\n')
            if SCRIPTING:
                sys.stderr.write('Program is being run in scripting mode with invalid or nonexistant config file, cannot continue.\n')
                sys.exit(1)
            else:
                return login_user()
    else:
        return login_user()

# @info - this logs the user into the API service by submitting their username and password in return for a temporary access
#         token. This token is stored in a hidden directory and can be loaded automatically when the user makes future requests.
def login_user() :
    print 'Please enter your Praxyk login credentials'
    USER_EMAIL = get_input('Email: ')
    USER_PASS = get_passwd()
    while not PRAXYK.login(email=USER_EMAIL, password=USER_PASS):
        print 'Invalid username/password combination, please check your credentials and try again, or type ^C to exit'
        USER_EMAIL = get_input('Email: ')
        USER_PASS = get_passwd()
    print 'Login successful!'
    user = PRAXYK.user().get()
    config = ConfigParser.ConfigParser()
    configfile = open(CLIENT_CONFIG_FILE, 'w+')
    config.add_section('default_section')
    config.set('default_section', 'auth_tok', '%s' % user.auth_token)
    config.write(configfile)
    return user

def register_user() :
    print 'Welcome to Praxyk!'
    print 'You are registering a new user account, if you do not wish to continue,' +\
        '\ntype ^C at any time to exit.'
    user_name = get_input('What is your name?')
    user_email = get_input('Please enter your email.')
    user_pass1 = get_passwd('Please enter your password.')
    user_pass2 = get_passwd('Please confirm your password.')
    while (user_pass1 != user_pass2) :
        print 'The passwords do not match, please enter matching passwords.'
        user_pass1 = get_passwd('Please enter your password.')
        user_pass2 = get_passwd('Please confirm your password.')
    if (not get_yes_no('Have you read and accepted our terms and conditions?\n' +\
        '(%s/terms_and_conditions.html)' % BASE_URL)) :
        print 'Feel free to come back if you change your mind.'
        exit_session()
    else :
        user = PRAXYK.user(name=user_name,email=user_email).post()
        if user :
            print 'Welcome, %s!' % user_name
            print 'You will need to confirm your account through your email before using our services.'
            exit_session()
        else :
            print 'Registration failed :(' # @TODO : put a reason why the registration failed
            if get_yes_no ('Would you like to attempt to register again?') :
                register_user()
            else :
                exit_session()

def exit_session() :
    print 'Thanks for using the Praxyk client script!'
    sys.exit(0)

def change_password(user=None) :
    pass

def change_email(user=None) :
    pass

def update_user(argv=None) :
    pass

def get_user(argv=None) :
    print PRAXYK.user.get()

def get_users(argv=None) :
    pass

def switch_user() :
    pass

def display_user() :
    pass

def apply_coupon() :
    pass

def begin_transaction() :
    pass

def cancel_transaction() :
    pass

def display_transactions() :
    pass

def display_transaction() :
    pass

def display_results() :
    pass

def display_result() :
    pass

# @info - this attempts to parse a command the user has typed in by matching it with the ACTION_MAP
# dictionary, and calls the appropriate function if the user's command is valid.
def parse_command(command) :
    if command == '' :
        return
    print 'command: ',command
    if not command.action or command.action not in ACTIONS :
        sys.stderr.write('Must include a valid action (%s)\n' % ACTIONS)
        return
    if not command.noun or command.noun not in NOUNS :
        sys.stderr.write('Must include a valid noun (%s)\n' % NOUNS)
        return
    action_func = ACTION_MAP.get(command.action).get(command.noun, None)
    if not action_fun :
        sys.stderr.write('It looks like your input of \'%s\' is invalid or not yet implemented.' +\
            ' If you feel this is an error, please contact the Praxyk team at %s\n' % ((command.action+' '+command.noun+' '+\
                +' '+command.specifics), BASE_URL))
        return
    res = action_func(argv=command.specifics)


ACTION_MAP = {
    'login'     : { ""  : login_user },

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

ACTIONS = ACTION_MAP.keys()
NOUNS = [ noun_func_pair.keys() for noun_func_pair in ACTION_MAP.values() ]

# @info - main function, loops to get user input and calls
# appropriate functions as per the user's command
if __name__ == "__main__" :
    try:
        set_up_env()
        PRAXYK = Praxyk()
        SCRIPTING = False
        args = parse_args(sys.argv)
        if args.root :
            CLIENT_CONFIG_FILE = CONFIG_DIR + 'root.config'
        USER = load_user()
        print GREETING

        command_parser = argparse.ArgumentParser()
        command_parser.add_argument('action', help='This argument is the action the user is requesting the script perform.' +\
            '\nIt can be one of the following: login, register, exit, switch, change, apply, begin, cancel, display')
        command_parser.add_argument('noun', nargs='?', default='', help='This argument is the specific noun the action should act on.' +\
            '\nIt can be one of the following, (with action in parenthesis), {switch} user, {change} email or password, {apply} coupon,' +\
            '{begin} transaction, {cancel} transaction, {display} user or transactions or transaction or results or result or users.')
        command_parser.add_argument('specifics', nargs='*', default=None, help='This (sometimes) optional argument contains the specifics' +\
            'of the user\'s command such as the transaction id of the transaction they want to display.')

        while (True):
            command = get_input('')
            parsed_command = command_parser.parse_args(command)
            parse_command(parsed_command)
    except KeyboardInterrupt:
        print '\n^C received, exiting the Praxyk client script.'
        sys.exit(0)
    except Exception as e:
        print 'Something bad happened...\nPlease take the time to forward the following trace to help@praxyk.com, thanks!'
        traceback.print_exc()
        sys.exit(1)
