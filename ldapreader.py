#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script de consultation d'un répertoire LDAP via l'API LDAPAdmin de geOrchestra.

Documentation: cf. readme.md.
"""

import os
import argparse
import ConfigParser
from libs import requests
from libs import vobject

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2015, CIGAL"
__credits__ = ["Guillaume Ryckelynck",]
__license__ = "GPL"
__version__ = "3.0.0"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@region-alsace.eu"
__status__ = "Production"

requests.packages.urllib3.disable_warnings()

# Authentification constants get from config file
parser = ConfigParser.ConfigParser()
parser.read('ldapreader.cfg')
LDAP_LOGIN = parser.get('LDAP', 'login')
LDAP_PWD = parser.get('LDAP', 'password')
SERVER_API_URL = parser.get('LDAP', 'server_url')


def getLdapUser(uid = None):
    """ Get LDAP user from server by uid. 
    """
    user = None
    ldap_keys = ['givenName', 'sn', 'o', 'title', 'postalAddress', 'telephoneNumber', 'mail', 'uid', 'employeeNumber', 'description']
    if uid is not None:
        r_user = requests.get(SERVER_API_URL + '/users/' + uid , auth=(LDAP_LOGIN, LDAP_PWD), verify=False)
        user = r_user.json()
        for k in ldap_keys: 
            if not k in user:
                user[k] = ''
        # Get user groups
        user['groups'] = []
        r_groups = requests.get(SERVER_API_URL + '/groups', auth=(LDAP_LOGIN, LDAP_PWD), verify=False)
        groups = r_groups.json()
        for group in groups:
            if user['uid'] in group['users'] and group['cn']:
                user['groups'].append(group['cn'])
    return user

def printLdapUser(user = None):
    """ Print LDAP user on sreen. 
    """
    if user is not None:
        print '*' * 79
        print 'UID (uid):'.ljust(30), user['uid']
        print 'Nom (sn):'.ljust(30), user['sn']
        print 'Prénom (givenName):'.ljust(30), user['givenName']
        print 'Organisme (o):'.ljust(30), user['o']
        print 'Fonction (title):'.ljust(30), user['title']
        print 'Adresse (postalAddress):'.ljust(30), user['postalAddress']
        print 'Tél. (telephoneNumber):'.ljust(30), user['telephoneNumber']
        print 'Email (mail):'.ljust(30), user['mail']
        print 'Description (description):'.ljust(30), user['description']
        print 'Groupes:'.ljust(30), ', '.join(user['groups'])
        print '*' * 79
    else:
        print "No user found."
            

def getLdapUsers(word = None, group = None):
    """ Get LDAP users list from server. 
    """
    result = []
    # Get all users dict
    r_users = requests.get(SERVER_API_URL + '/users', auth=(LDAP_LOGIN, LDAP_PWD), verify=False)
    users = r_users.json()
    
    # Get all users list
    users_all = [user['uid'] for user in users]
    
    # Get users to keep from group (else, all users)
    keep_users_group = users_all
    if group is not None:
        keep_users_group = []
        r_groups = requests.get(SERVER_API_URL + '/groups', auth=(LDAP_LOGIN, LDAP_PWD), verify=False)
        for ldap_group in r_groups.json():
            if group.lower() in ldap_group['cn'].lower():
                keep_users_group.extend(ldap_group['users'])
        keep_users_group = list(set(keep_users_group))

    # Get users to keep from word (else, all users)
    keep_users_word = users_all
    if word is not None:
        keep_users_word = []
        for user in users:
            if 'o' not in user: user['o'] = ''
            user_str = ' '.join([user['uid'], user['sn'], user['givenName'], user['o']])
            if word.lower() in user_str.lower():
                keep_users_word.append(user['uid'])

    # Compare users from word and users from group
    keep_users = list(set(keep_users_group) & set(keep_users_word))
    
    # Get users detail from keep users
    for user in users:
        for keep_user in keep_users:
            if user['uid'] == keep_user:
                result.append(user)

    return result
    
def printLdapUsers(users = None):
    """ Print LDAP users list on sreen. 
    """
    if users:
        print '-' * 79
        print '| ', 'UID'.ljust(20), ' | ', 'SN'.ljust(20), ' | ', 'GIVEN NAME'.ljust(23), ' |'
        print '-' * 79
        for user in users:
            print '| ', user['uid'].ljust(20), ' | ', user['sn'].ljust(20), ' | ', user['givenName'].ljust(23), ' |'
            #print '-' * 79
        print '-' * 79
        print len(users), " users found."
    else:
        print "No user found."

def getLdapgroups(word = None):
    """ Get LDAP groups from server. 
    """
    # Get all groups
    r_groups = requests.get(SERVER_API_URL + '/groups', auth=(LDAP_LOGIN, LDAP_PWD), verify=False)
    groups = r_groups.json()
    result = groups
    
    if word is not None:
        result = []
        for group in groups:
            if not 'description' in group: 
                group['description'] = ''
            group_str = ' '.join([group['cn'], group['description']])
            if word in group_str:
                result.append(group)
    
    return result
    
def printLdapGroups(groups = None):
    """ Print LDAP groups list on sreen. 
    """
    if groups:
        print '-' * 79
        print '| ', 'CN'.ljust(25), ' | ', 'DESCRIPTION'.ljust(43), ' | '
        print '-' * 79
        for group in groups:
            if 'description' not in group: group['description'] = ''
            print '| ', group['cn'].ljust(25), ' | ', group['description'].ljust(43), ' | '
            #print '-' * 79
        print '-' * 79
        print len(groups), " groups found."
    else:
        print "No group found."

def vcardLdapUser(user = None):
    """ Generate VCARD txt file from a user. 
    """
    ldap_keys = ['givenName', 'sn', 'o', 'title', 'postalAddress', 'telephoneNumber', 'mail', 'uid', 'employeeNumber', 'description']
    for k in ldap_keys:
        if not k in user.keys():
            user[k] = ''
        
    j = vobject.vCard()

    o= j.add('uid')
    o.value = user['uid']
    
    o= j.add('fn')
    o.value = user['givenName'] + ' ' + user['sn']

    o = j.add('n')
    o.value = vobject.vcard.Name(family= user['sn'], given=user['givenName'] )

    o= j.add('email')
    o.type_param = 'INTERNET'
    o.value = user['mail']

    o=j.add('org')
    o.value = [user['o']]
    
    o= j.add('role')
    o.value = user['title']

    o= j.add('tel')
    o.type_param = 'WORK'
    o.value = user['telephoneNumber']   

    o=j.add ('adr')
    o.type_param = 'BUSINESS'
    o.value.street  = user['postalAddress']
    
    user_groups = []
    if 'groups' in user:
        user_groups = user['groups']

    o=j.add('categories')
    #user['groups'].append('A traiter')
    o.value = user_groups

    o=j.add('note')
    o.value = 'LDAP uid: ' + user['uid'] + '\n\n' + 'LDAP description: ' + user['description'] + '\n\n' + 'Groupes: ' + ', '.join(user_groups)

    return j.serialize()

if __name__ == "__main__": 
    # Commande line: list of arguments/options
    parser = argparse.ArgumentParser(description='Ldapadmin reader.')
    parser.add_argument('action', help='verbose flag')
    parser.add_argument('--uid', '-u', help='User id')
    parser.add_argument('--word', '-w', help='word to search in user list')
    parser.add_argument('--group', '-g', help='group to search in user list')
    parser.add_argument('--vcard', '-c', help='vcard path/filename export')
    parser.add_argument('--vctype', '-t', help='type of vcard to export (m = multi / s = simple)')
    args = parser.parse_args()

    # Main program
    if args.action in ['user', 'users', 'groups']:
        if args.action == 'user':
            if args.uid:
                user_data = getLdapUser(args.uid)
                if args.vcard:
                    if os.path.isdir(args.vcard):
                        filename = os.path.join(args.vcard, user_data['uid'] + '.vcf')
                        vcard = vcardLdapUser(user_data)
                        with open(filename, 'wb') as file:
                            file.write(vcard)
                        print "Ok: vcard file " + filename + " created."
                    else:
                        print "Error: path '" + args.vcard + "' doesn't exist. thanks to create directories."
                else:
                    printLdapUser(user_data)
            else:
                print "Error: '--uid/-u <uid>' argument is required."
                
        if args.action == 'users':
            users = getLdapUsers(args.word, args.group)
            if args.vcard:
                if not args.vctype or args.vctype == 'm':
                    if os.path.isdir(os.path.dirname(args.vcard)):
                        vcard = []
                        for user in users:
                            user_data = getLdapUser(user['uid'])
                            vcard.append(vcardLdapUser(user_data))
                        with open(args.vcard, 'wb') as file:
                            file.write ('\n'.join(vcard))
                        print "Ok: vcard file " + args.vcard + " created."
                    else:
                        print "Error: path '" + os.path.dirname(args.vcard) + "' doesn't exist. thanks to create directory."

                elif args.vctype == 's':
                    if os.path.isdir(args.vcard):
                        for user in users:
                            user_data = getLdapUser(user['uid'])
                            filename = os.path.join(args.vcard, user['uid'] + '.vcf')
                            vcard = vcardLdapUser(user_data)
                            with open(filename, 'wb') as file:
                                file.write (vcard)
                            print "Ok: vcard files " + filename + " created."
                    else:
                        print "Error: path '" + args.vcard + "' doesn't exist. thanks to create directory."
                    
                else:
                    print "Error: invalid value for vcard type (--vctype/-t). Choose 'm' (multiple) or 's' (simple)."

            else:
                printLdapUsers(users)

        if args.action == 'groups':
            groups = getLdapgroups(args.word)
            printLdapGroups(groups)
        
    else:
        print "Error: invalid value for action. Choose 'user', 'users' or 'groups'."

