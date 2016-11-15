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
__module__ = "update-vpn-endpoint"
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


def updateVpnEndpoint(endpoint, resourcename, cookie, name, customervpngateway, psk, reachableroutes, enabled=False):
    basepath = '/vpnendpoint/'
    params = None
    data = {"name": name, "customer_vpn_gateway": str(customervpngateway), "psk": str(psk),
            "reachable_routes": str(reachableroutes)}
    if enabled is not None:
        data['enabled'] = enabled
    response = callRESTApi(endpoint, basepath, resourcename, data, 'PUT', params, cookie)
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
    moduleArgs['customervpngateway'] = None
    moduleArgs['psk'] = None
    moduleArgs['reachableroutes'] = None
    moduleArgs['enabled'] = False

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
        elif opt in ("-g", "--customervpngateway"):
            moduleArgs['customervpngateway'] = arg
        elif opt in ("-k", "--psk"):
            moduleArgs['psk'] = arg
        elif opt in ("-r", "--reachableroutes"):
            moduleArgs['reachableroutes'] = arg
        elif opt in ("-E", "--enabled"):
            moduleArgs['enabled'] = True

    return moduleArgs


# Main processing function
def main(argv):
    # Configure Parameters and Options
    options = 'e:u:p:P:R:C:D:n:d:'
    longOptions = ['endpoint=', 'user=', 'password=', 'pwdfile=', 'resourcename=', 'cookie=', 'description=',
                   'name=', 'default=']
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
            jsonObj = updateVpnEndpoint(moduleArgs['endpoint'], moduleArgs['resourcename'], moduleArgs['cookie'],
                                        moduleArgs['name'], moduleArgs['customervpngateway'], moduleArgs['psk'],
                                        moduleArgs['reachableroutes'], moduleArgs['enabled'])
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
