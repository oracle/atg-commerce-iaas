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
__module__ = "create-storage-volume"
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


def createStorageVolume(endpoint, resourcename, cookie, size, name, properties=["/oracle/public/storage/default"], bootable=False, imagelist=None, imagelistentry=None,
                        description=None, tags=None, snapshot=None, **kwargs):
    basepath = '/storage/volume/'
    params = None
    data = {"size": size, "properties": properties, "name": name, "bootable": bootable}
    if imagelist is not None:
        data['imagelist'] = imagelist
    if imagelistentry is not None:
        data['imagelistentry'] = imagelistentry
    if description is not None:
        data['description'] = description
    if tags is not None:
        data['tags'] = tags
    if snapshot is not None:
        data['snapshot'] = snapshot
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
    moduleArgs['size'] = None
    moduleArgs['name'] = None
    moduleArgs['imagelist'] = None
    moduleArgs['imagelistentry'] = None
    moduleArgs['bootable'] = False
    moduleArgs['tags'] = None
    moduleArgs['snapshot'] = None
    moduleArgs['properties'] = ["/oracle/public/storage/default"]

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
        elif opt in ("-s", "--size"):
            moduleArgs['size'] = arg
        elif opt in ("-n", "--name"):
            moduleArgs['name'] = arg
        elif opt in ("-D", "--description"):
            moduleArgs['description'] = arg
        elif opt in ("-i", "--imagelist"):
            moduleArgs['imagelist'] = arg
        elif opt in ("-E", "--imagelistentry"):
            moduleArgs['imagelistentry'] = arg
        elif opt in ("-b", "--bootable"):
            moduleArgs['bootable'] = True
        elif opt in ("-t", "--tags"):
            moduleArgs['tags'] = arg
        elif opt in ("-S", "--snapshot"):
            moduleArgs['snapshot'] = arg
        elif opt in ("--properties"):
            moduleArgs['properties'] = arg.split(',')
    return moduleArgs


# Main processing function
def main(argv):
    # Configure Parameters and Options
    options = 'e:u:p:P:R:C:D:s:n:i:E:bt:S:'
    longOptions = ['endpoint=', 'user=', 'password=', 'pwdfile=', 'resourcename=', 'cookie=', 'description=', 'size=',
                   'name=', 'imagelist=', 'imagelistentry=', 'bootable', 'tags=', 'properties=', 'snapshot=']
    # Get Options & Arguments
    try:
        opts, args = getopt.getopt(argv, options, longOptions)
        # Read Module Arguments
        moduleArgs = readModuleArgs(opts, args)

        if moduleArgs['cookie'] is None and moduleArgs['endpoint'] is not None and moduleArgs['user'] is not None:
            if moduleArgs['password'] is None and moduleArgs['pwdfile'] is None:
                moduleArgs['password'] = getPassword(moduleArgs['user'])
            elif moduleArgs['pwdfile'] is not None:
                with open(moduleArgs['pwdfile'], 'r') as f:
                    moduleArgs['password'] = f.read().rstrip('\n')
            moduleArgs['cookie'] = authenticate(moduleArgs['endpoint'], moduleArgs['user'], moduleArgs['password'])
        if moduleArgs['cookie'] is not None:
            jsonObj = createStorageVolume(moduleArgs['endpoint'], moduleArgs['resourcename'], moduleArgs['cookie'],
                                          moduleArgs['size'], moduleArgs['name'], moduleArgs['properties'], moduleArgs['bootable'], moduleArgs['imagelist'], moduleArgs['imagelistentry'], moduleArgs['description'], moduleArgs['tags'], moduleArgs['snapshot'])
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
