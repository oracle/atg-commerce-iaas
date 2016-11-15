#!/usr/bin/python
# Copyright (c) 2013, 2014-2016 Oracle and/or its affiliates. All rights reserved.


"""Provide Module Description
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Andrew Hopkinson (Oracle Cloud Solutions A-Team)"
__copyright__ = "Copyright (c) 2013, 2014-2016  Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "create-security-rule"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import datetime
import getopt
import json
import locale
import logging
import operator
import os
import requests
import sys

# Import utility methods


from occsutils import callRESTApi
from occsutils import getPassword
from occsutils import printJSON
from authenticate import authenticate


# Define methods


def createSecurityRule(endpoint, resourcename, cookie, name, srclist, dstlist, application, action='PERMIT',
                       description=None, disabled=False, **kwargs):
    basepath = '/secrule/'
    params = None
    data = {"name": name, "src_list": str(srclist), "dst_list": str(dstlist), "application": str(application),
            "action": str(action)}
    if description is not None:
        data['description'] = description
    else:
        data['description'] = name
    if disabled is not None:
        data['disabled'] = disabled
    response = callRESTApi(endpoint, basepath, resourcename, data, 'POST', params, cookie)
    jsonResponse = json.loads(response.text)
    return jsonResponse


# Read Module Arguments
def readModuleArgs(opts, args):
    moduleArgs = {}
    moduleArgs['endpoint'] = None
    moduleArgs['user'] = None
    moduleArgs['password'] = None
    moduleArgs['pwdfile'] = None
    moduleArgs['resourcename'] = None
    moduleArgs['cookie'] = None
    moduleArgs['name'] = None
    moduleArgs['description'] = None
    moduleArgs['srclist'] = None
    moduleArgs['dstlist'] = None
    moduleArgs['application'] = None
    moduleArgs['name'] = None
    moduleArgs['action'] = False

    # Read Module Command Line Arguments.
    for opt, arg in opts:
        if opt in ("-e", "--endpoint"):
            moduleArgs['endpoint'] = arg
        elif opt in ("-u", "--user"):
            moduleArgs['user'] = arg
        elif opt in ("-p", "--password"):
            moduleArgs['password'] = arg
        elif opt in ("-P", "--pwdfile"):
            moduleArgs['pwdfile'] = arg
        elif opt in ("-R", "--resourcename"):
            moduleArgs['resourcename'] = arg
        elif opt in ("-C", "--cookie"):
            moduleArgs['cookie'] = arg
        elif opt in ("-n", "--name"):
            moduleArgs['name'] = arg
        elif opt in ("-D", "--description"):
            moduleArgs['description'] = arg
        elif opt in ("-s", "--srclist"):
            moduleArgs['srclist'] = arg
        elif opt in ("-l", "--dstlist"):
            moduleArgs['dstlist'] = arg
        elif opt in ("-A", "--application"):
            moduleArgs['application'] = arg
        elif opt in ("-a", "--action"):
            moduleArgs['action'] = arg
        elif opt in ("-d", "--disabled"):
            moduleArgs['disabled'] = True

    return moduleArgs


# Main processing function
def main(argv):
    # Configure Parameters and Options
    options = 'e:u:p:P:R:C:D:n:s:l:A:a:d'
    longOptions = ['endpoint=', 'user=', 'password=', 'pwdfile=', 'resourcename=', 'cookie=', 'description=',
                   'name=', 'srclist=', 'dstlist=', 'application=', 'action=', 'disabled']
    # Get Options & Arguments
    try:
        opts, args = getopt.getopt(argv, options, longOptions)
        # Read Module Arguments
        moduleArgs = readModuleArgs(opts, args)
        printJSON(moduleArgs)

        if moduleArgs['cookie'] is None and moduleArgs['endpoint'] is not None and moduleArgs['user'] is not None:
            if moduleArgs['password'] is None and moduleArgs['pwdfile'] is None:
                moduleArgs['password'] = getPassword(moduleArgs['user'])
            elif moduleArgs['pwdfile'] is not None:
                with open(moduleArgs['pwdfile'], 'r') as f:
                    moduleArgs['password'] = f.read().rstrip('\n')
            moduleArgs['cookie'] = authenticate(moduleArgs['endpoint'], moduleArgs['user'], moduleArgs['password'])
        if moduleArgs['cookie'] is not None:
            jsonObj = createSecurityRule(moduleArgs['endpoint'], moduleArgs['resourcename'], moduleArgs['cookie'],
                                         moduleArgs['name'], moduleArgs['srclist'], moduleArgs['dstlist'],
                                         moduleArgs['application'], moduleArgs['action'], moduleArgs['description'],
                                         moduleArgs['disabled'])
            printJSON(jsonObj)
        else:
            print ('Incorrect parameters')
    except getopt.GetoptError:
        usage()
    except Exception as e:
        print('Unknown Exception please check log file')
        logging.exception(e)
        sys.exit(1)

    return


# Main function to kick off processing
if __name__ == "__main__":
    main(sys.argv[1:])
