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
from libs.python.praxyk import Praxyk
from libs.python.praxyk.pod import pod_ocr, pod_bayes_spam, pod_face_detect
from libs.python.praxyk import result
from libs.python.praxyk import results

from os.path import expanduser

global CONFIG_DIR
global CLIENT_CONFIG_FILE
global USER_AUTH
global USER_EMAIL
global USER_PASS
global PRAXYK
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
                login_user()
                return
        else:
            answer = get_yes_no('Would you like to load user data from the Praxyk config file?')

    if answer or SCRIPTING:
        try:
            config = ConfigParser.ConfigParser()
            configfile = open(CLIENT_CONFIG_FILE, 'r')
            config.readfp(configfile)
            #print 'CONFIG: ',config.get('default_section','email')
            answer = get_yes_no('Would you like to use the credentials for the account associated with the email %s?' % config.get('default_section','email'))
            if answer :
                USER_AUTH = config.get('default_section', 'auth_tok')
                if not PRAXYK.login(auth_token=USER_AUTH): # @TODO add support for changing the config section to load
                    print 'Unable to log in using the default credentials in config file, please log in with fresh credentials, ' +\
                        'or type ^C to exit.'
                    login_user()
                    return
                else :
                    print 'Successfully logged in using credentials from config file.'
            else :
                login_user
                return
        except Exception:
            sys.stderr.write('Unable to open the local configuration file.\n')
            if SCRIPTING:
                sys.stderr.write('Program is being run in scripting mode with invalid or nonexistant config file, cannot continue.\n')
                sys.exit(1)
            else:
                login_user()
                return
    else:
        login_user()
        return

# @info - this logs the user into the API service by submitting their username and password in return for a temporary access
#         token. This token is stored in a hidden directory and can be loaded automatically when the user makes future requests.
def login_user(argv=None) :
    print 'Please enter your Praxyk login credentials'
    USER_EMAIL = get_input('Email: ')
    USER_PASS = get_passwd()
    while not PRAXYK.login(email=USER_EMAIL, password=USER_PASS):
        print 'Invalid username/password combination, please check your credentials and try again, or type ^C to exit'
        USER_EMAIL = get_input('Email: ')
        USER_PASS = get_passwd()
    print 'Login successful!'
    PRAXYK.user().get()
    config = ConfigParser.ConfigParser()
    configfile = open(CLIENT_CONFIG_FILE, 'w+')
    config.add_section('default_section')
    config.set('default_section', 'auth_tok', '%s' % user.auth_token)
    config.set('default_section', 'email', '%s' % user.email)
    config.write(configfile)

def register_user(argv=None) :
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

def exit_session(argv=None) :
    print 'Thanks for using the Praxyk client script!'
    sys.exit(0)

def change_password(user=None) :
    new_pass1 = get_passwd('Please enter your new password.')
    new_pass2 = get_passwd('Please confirm your new password.')
    while (user_pass1 != user_pass2) :
        print 'The passwords do not match, please enter matching passwords.'
        new_pass1 = get_passwd('Please enter your new password.')
        new_pass2 = get_passwd('Please confirm your new password.')
    response = PRAXYK.user().post(new_pass1)
    if not response :
        print 'Unable to complete your request to change password.\n'
        return
    else :
        print 'Password changed successfully.'
        return


def change_email(user=None) :
    print 'This is not currently supported through our API, sorry about that!'
    return

def update_user(argv=None) :
    PRAXYK.user().get()
    return

def get_user(argv=None) :
    PRAXYK.user().get()
    return

def switch_user(argv=None) :
    return

def display_users(argv=None) :
    print 'This action is only supported for admin accounts, and ' +\
        'is not even supported yet.'
    return

def display_user(argv=None) :
    get_user()
    user_dict = PRAXYK.user().to_dict()
    user_auth = user_dict.get('auth_token')
    user_dict = user_dict.get('caller')
    #print 'USER_DICT: ',user_dict
    print '\n\tUser information for %s:' % user_dict.get('name')
    for key,value in user_dict.items() :
        print '\t\t-',key.ljust(20),': ',str(value).ljust(15)
    print '' # for formatting, yes I know it looks dumb but I just need one newline
    pass

def apply_coupon(argv=None) :
    print 'Sorry, coupons are not currently supported through the Praxyk client script.'
    """
    if not argv :
        coupon_id = get_input('Please specify the coupon code to apply')
    else :
        coupon_id = argv
    """
    return

SERVICES = ['ocr', 'face_detect', 'spam']

def begin_transaction(argv=None) :
    try :
        service = ''
        query = argv.split(' ')
        if len(query) < 2 or str(query[0]).lower() not in SERVICES :
            print 'To begin a transaction you need to specify a service (ocr, face_detect, spam) and a file or series of files to upload.'
            while (query[0].lower() not in SERVICES or len(query) < 2) :
                query = get_input('Please enter the service you would like to use followed by at least one file to upload: ').split(' ')
        service = query.pop(0)
        if service == 'ocr' :
            p = pod_ocr.POD_OCR(PRAXYK)
        elif service == 'face_detect' :
            p = pod_face_detect.POD_FaceDetect(PRAXYK)
        elif service == 'spam' :
            p = pod_bayes_spam.POD_BayesSpam(PRAXYK)
        res = p.post(file_names=query)
        return
    except Exception as e:
        print e
        return

def cancel_transaction(argv=None) :
    trans_id = argv
    if trans_id is None :
        trans_id = get_input('Enter the id of the transaction you would like to cancel: ')
    result = PRAXYK.transaction(trans_id=trans_id).put(cancel=True)
    print 'RESULT: ',result
    if not result :
        print 'SOMETHING BAD HAPPENED'
    return

def display_transactions(argv=None) :
    get_user()
    response = True
    transactions = PRAXYK.user().transactions().get()
    if len(transactions.to_dict()) > 0 :
        print '\n\tTransactions:'
        for transaction in transactions.to_dict().get('transactions') :
            print_div()
            print_dict(transaction)
        print_div()
    else :
        print 'No transactions to display, try starting a transaction now!'
    return

def display_transaction(argv=None) :
    get_user()
    trans_id = argv
    if trans_id is None :
        trans_id = get_input('Please enter the id of the transaction you would like to view: ')
    try :
        transaction = PRAXYK.user().transaction(trans_id=trans_id)

        if not transaction.get() :
            print 'The transaction with id \'%s\' does not exist' % trans_id
        trans_dict = transaction.to_dict()
        if len(trans_dict) > 0 :
            print '\n\tTransaction:'
            print_div()
            print_dict(trans_dict)
            print_div()
        else :
            print 'The transaction ',transaction_id,' does not exist.'
        return
    except :
        print 'Error retreiving information about the transaction with id \'%s\'.' % trans_id
        print 'It is possible this is a transaction that does not belong to you or is not a valid id.'
        return

def display_results(argv=None) :
    pass

def display_result(argv=None) :
    if argv is None :
        trans_id = get_input('Please enter the transaction id of the result you wish to view: ')
    else :
        trans_id = argv
    result = praxykResult(trans_id=trans_id).get()
    if result is None :
        print 'Unable to get the results of transaction with id %s, check to make sure the transaction ' +\
            'id you have entered is correct.' % trans_id
    else :
        print 'Result:'
        print_div()
        print result
        print_div()
    return

# @info - this attempts to parse a command the user has typed in by matching it with the ACTION_MAP
# dictionary, and calls the appropriate function if the user's command is valid.
def parse_command(command) :
    if command == '' :
        return
    command_list = command.split(' ',2)
    num_args = len(command_list)
    action=noun=specifics=''
    #print 'command_list: ',command_list,' length {',num_args,'}'
    action = command_list[0]
    #print 'action: ',action
    if num_args > 1:
        noun = command_list[1]
        #print 'noun: ',noun
    if num_args > 2:
        specifics = command_list[2]
        #print 'specifics: ',specifics
    if action not in ACTIONS :
        sys.stderr.write('Must include a valid action (%s)\n' % ACTIONS)
        return
    if noun not in NOUNS :
        print '' in NOUNS
        print not ''
        sys.stderr.write('Must include a valid noun (%s)\n' % NOUNS)
        return
    action_func = ACTION_MAP.get(action).get(noun, None)
    if not action_func :
        sys.stderr.write('It looks like your input of \'%s\' is invalid or not yet implemented.' +\
            ' If you feel this is an error, please contact the Praxyk team at %s\n' % ((action+' '+noun+' '+\
                +' '+specifics), BASE_URL))
        return
    res = action_func(argv=specifics)

def print_div(char='-') :
    print str(char) * 80

def print_dict(dictionary) :
    for key,value in dictionary.items() :
        if key != 'auth_token' :
            if type(value) is dict :
                print '\t-',str(key).ljust(20)
                print_dict(value)
            else :
                print '\t-',str(key).ljust(20),': ',str(value).ljust(20)

def print_help(argv=None) :
    print 'Valid actions followed by valid nouns to be used in conjunction with them:'
    print_div()
    for key,value in ACTION_MAP.items() :
        print 'Action: ',key
        for key in value.keys() :
            print '\t\tNoun: ',key
    print_div()
    return

ACTION_MAP = {
    'help'      : { ""  : print_help },

    'login'     : { ""  : login_user }, #

    'register'  : { ""  : register_user }, #

    'exit'      : { ""  : exit_session }, #

    'switch'    : { "user" : switch_user },

    'change'    : {
                    "email" : change_email, #
                 "password" : change_password }, #

    'apply'      : {
                    "coupon": apply_coupon }, #

    'begin'      : {
               "transaction": begin_transaction }, #

    'cancel'     : {
              "transaction" : cancel_transaction }, #

    'display'    : { "users" : display_users, #
                      "user" : display_user, #
              "transactions" : display_transactions, #
               "transaction" : display_transaction, #
                   "results" : display_results,
                    "result" : display_result } }

ACTIONS = ACTION_MAP.keys()
NOUNS = []

# @info - main function, loops to get user input and calls
# appropriate functions as per the user's command
if __name__ == "__main__" :
    try:
        set_up_env()
        for noun_func_pair in ACTION_MAP.values():
                keys = noun_func_pair.keys()
                for key in keys:
                    if key not in NOUNS:
                        NOUNS.append(key)
        PRAXYK = Praxyk()
        SCRIPTING = False
        args = parse_args(sys.argv)
        if args.root :
            CLIENT_CONFIG_FILE = CONFIG_DIR + 'root.config'
        load_user()
        print GREETING
        while (True):
            command = get_input('')
            parse_command(command)
    except KeyboardInterrupt:
        print '\n^C received, exiting the Praxyk client script.'
        sys.exit(0)
    except Exception as e:
        print 'Something bad happened...\nPlease take the time to forward the following trace to help@praxyk.com, thanks!'
        print e
        #traceback.print_exc()
        sys.exit(1)
