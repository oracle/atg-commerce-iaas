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
__module__ = "create-security-application"
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


def createSecurityApplication(endpoint, resourcename, cookie, name, protocol, description=None, dport=None,
                              imcptype=None, imcpcode=None, **kwargs):
    basepath = '/secapplication/'
    params = None
    data = {"name": name, "protocol": str(protocol)}
    if description is not None:
        data['description'] = description
    if dport is not None:
        data['dport'] = dport
    if imcptype is not None:
        data['imcptype'] = imcptype
    if imcpcode is not None:
        data['imcpcode'] = imcpcode
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
    moduleArgs['description'] = None
    moduleArgs['name'] = None
    moduleArgs['protocol'] = None
    moduleArgs['dport'] = None
    moduleArgs['icmptype'] = None
    moduleArgs['icmpcode'] = None

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
        elif opt in ("-r", "--protocol"):
            moduleArgs['protocol'] = arg
        elif opt in ("-d", "--dport"):
            moduleArgs['dport'] = arg
        elif opt in ("-t", "--icmptype"):
            moduleArgs['icmptype'] = arg
        elif opt in ("-c", "--icmpcode"):
            moduleArgs['icmpcode'] = arg

    return moduleArgs


# Main processing function
def main(argv):
    # Configure Parameters and Options
    options = 'e:u:p:P:R:C:D:n:r:d:t:c:'
    longOptions = ['endpoint=', 'user=', 'password=', 'pwdfile=', 'resourcename=', 'cookie=', 'name=', 'description=',
                   'protocol=', 'dport=', 'icmptype=', 'icmpcode=']
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
            jsonObj = createSecurityApplication(moduleArgs['endpoint'], moduleArgs['resourcename'],
                                                moduleArgs['cookie'],
                                                moduleArgs['name'], moduleArgs['protocol'], moduleArgs['description'],
                                                moduleArgs['dport'], moduleArgs['icmptype'], moduleArgs['icmpcode'])
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
