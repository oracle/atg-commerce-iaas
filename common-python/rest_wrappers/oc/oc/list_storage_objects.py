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
__module__ = "list_storage_object"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import datetime
import getopt
import hashlib
import json
import locale
import logging
import operator
import os
import requests
import subprocess
import sys
import tempfile
from contextlib import closing

# Import utility methods


from oscsutils import callRESTApi
from oscsutils import getPassword
from oscsutils import printJSON
from authenticate_oscs import authenticate


# Define methods
def listStorageObjects(endpoint, resourcename, authtoken, limit=None, marker=None, end_marker=None, format=None, prefix=None, delimiter=None, **kwargs):
    basepath = ''
    headers = None
    params = {}
    if limit is not None:
        params['limit'] = limit
    if marker is not None:
        params['marker'] = marker
    if end_marker is not None:
        params['end_marker'] = end_marker
    if format is not None:
        params['format'] = format
    if prefix is not None:
        params['prefix'] = prefix
    if delimiter is not None:
        params['delimiter'] = delimiter
    data = None
    files = None
    response = callRESTApi(endpoint, basepath, resourcename, method='GET', authtoken=authtoken, headers=headers, params=params, data=data, files=files)
    jsonResponse = response.text
    return jsonResponse


# Read Module Arguments
def readModuleArgs(opts, args):
    moduleArgs = {}
    moduleArgs['endpoint'] = None
    moduleArgs['user'] = None
    moduleArgs['password'] = None
    moduleArgs['pwdfile'] = None

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
    return moduleArgs


# Main processing function
def main(argv):
    # Configure Parameters and Options
    options = 'e:u:p:P:'
    longOptions = ['endpoint=', 'user=', 'password=', 'pwdfile=']
    # Get Options & Arguments
    try:
        opts, args = getopt.getopt(argv, options, longOptions)
        # Read Module Arguments
        moduleArgs = readModuleArgs(opts, args)
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
