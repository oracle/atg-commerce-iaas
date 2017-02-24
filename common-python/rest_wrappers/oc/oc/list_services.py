#!/usr/bin/python
# Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved.

"""List PSM Service
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Eder Zechim (Oracle Cloud Solutions A-Team)"
__copyright__ = "Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "list_services"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# import datetime
# import hashlib
# import locale
# import logging
# import operator
# import subprocess
# import tempfile
# import base64
# from contextlib import closing
import getopt
import logging
import json
import requests
import sys

# Import utility methods
from occsutils import getPassword
from occsutils import printJSON
from connection import PSMConnection

# Define methods
def listServices(connection):
    response = connection.callrest(method='GET')
    jsonResponse = json.loads(response.text)
    return jsonResponse

# Read Module Arguments
def readModuleArgs(opts, args):
    moduleArgs = {}
    moduleArgs['endpoint'] = None
    moduleArgs['user'] = None
    moduleArgs['password'] = None
    moduleArgs['pwdfile'] = None
    moduleArgs['service'] = None
    moduleArgs['tenant'] = None
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
        elif opt in ("-s", "--service"):
            moduleArgs['service'] = arg            
        elif opt in ("-t", "--tenant"):
            moduleArgs['tenant'] = arg            
    return moduleArgs

# Main processing function
def main(argv):
    # Configure Parameters and Options
    options = 'e:u:p:P:s:t:'
    longOptions = ['endpoint=', 'user=', 'password=', 'pwdfile=', 'service=', 'tenant=']    
    # Get Options & Arguments
    try:
        opts, args = getopt.getopt(argv, options, longOptions)
        # Read Module Arguments
        moduleArgs = readModuleArgs(opts, args)
        if moduleArgs['endpoint'] is not None and moduleArgs['user'] is not None and moduleArgs['service'] is not None and moduleArgs['tenant'] is not None:
            if moduleArgs['password'] is None and moduleArgs['pwdfile'] is None:
                moduleArgs['password'] = getPassword(moduleArgs['user'])
            elif moduleArgs['pwdfile'] is not None:
                with open(moduleArgs['pwdfile'], 'r') as f:
                    moduleArgs['password'] = f.read().rstrip('\n')
            psmConn = PSMConnection(moduleArgs['endpoint'], moduleArgs['user'], moduleArgs['password'], service=moduleArgs['service'], tenant=moduleArgs['tenant'])
            jsonObj = listServices(psmConn)
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
