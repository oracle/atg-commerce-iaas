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
__module__ = "upload_storage_object"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import datetime
import getopt
import hashlib
import json
import locale
import logging
import multiprocessing
import operator
import os
import requests
import shutil
import subprocess
import sys
import tempfile
from contextlib import closing

# Import utility methods


from oscsutils import callRESTApi
from oscsutils import getPassword
from oscsutils import printJSON
from authenticate_oscs import authenticate
from oc_exceptions import REST401Exception

# Define methods
def md5(fname, readbuf=104857600, **kwargs):
    hash_md5 = hashlib.md5()
    cnt = 1
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(readbuf), b""):
            hash_md5.update(chunk)
            #print('Chunk: '+str(cnt))
            cnt +=1
    return hash_md5.hexdigest()


def getsplitprefix(filename):
    return os.path.split(filename)[-1] + '-'


def getsplitdir(filename):
    return filename + '.split'


def splitfile(filename, size='5GB', **kwargs):
    files = []
    if filename is not None:
        splitdir = getsplitdir(filename)
        os.makedirs(splitdir)
        prefix = os.path.join(splitdir, getsplitprefix(filename))
        cmd = ['split', '-b', size, filename, prefix]
        cmdEnv = dict(os.environ)
        outputLines = []
        with closing(tempfile.TemporaryFile()) as fout:
            try:
                outputLines = subprocess.check_output(cmd, env=cmdEnv, stderr=fout).splitlines()
            except subprocess.CalledProcessError as e:
                fout.flush()
                fout.seek(0)
                print(fout.read())
                print('\n'.join(outputLines))
                raise e
        return [os.path.join(splitdir, fn) for fn in os.listdir(splitdir)]


def uploadfile((endpoint, basepath, authtoken, filename, authendpoint, user, password)):
    print('Uploading : ' + filename)
    headers = None
    params = None
    files = None
    resourcename = os.path.split(filename)[-1]
    try:
        with closing(open(filename, 'rb')) as f:
            response = callRESTApi(endpoint, basepath, resourcename, method='PUT', authtoken=authtoken, headers=headers, params=params, data=f, files=files)
    except REST401Exception as e:
        # Reauthenticate and retry
        if authendpoint is not None and user is not None and password is not None:
            authtoken, endpoint = authenticate(authendpoint, user, password)
            with closing(open(filename, 'rb')) as f:
                response = callRESTApi(endpoint, basepath, resourcename, method='PUT', authtoken=authtoken, headers=headers, params=params, data=f, files=files)
        else:
            raise
    print('Uploaded  : ' + filename)
    return


def uploadStorageObject(endpoint, container='compute_images', authtoken=None, filename=None, splitsize=4000, poolsize=4, authendpoint=None, user=None, password=None, **kwargs):
    basepath = container
    imgbasepath = basepath
    splitbasepath = basepath + '_segments'
    headers = None
    params = None
    data = None
    files = None
    jsonResponse = ''
    if filename is not None and os.path.exists(filename):
        #md5hash = md5(filename)
        filesize = os.path.getsize(filename)
        filesize /= (1024 * 1024)
        if filesize > splitsize:
            print('Splitting : ' + filename)
            filelist = splitfile(filename, str(splitsize) + 'MB')
            print('Into ' + str(len(filelist)) + ' segments')
            basepath = splitbasepath + '/' + os.path.split(filename)[-1] + '/_segment_'
            pool = multiprocessing.Pool(poolsize)
            # Build tupal list
            workerdata = []
            for fn in filelist:
                workerdata.append([endpoint, basepath, authtoken, fn, authendpoint, user, password])
            #print(workerdata)
            # Start processes
            pool.map(uploadfile, workerdata)
            # Upload manifest file to point to parts
            manifest = basepath + '/' + getsplitprefix(filename)
            resourcename = os.path.split(filename)[-1]
            headers = {'Content-Length': 0, 'X-Object-Manifest': manifest}
            printJSON(headers)
            data = None
            basepath = imgbasepath
            try:
                response = callRESTApi(endpoint, basepath, resourcename, method='PUT', authtoken=authtoken, headers=headers, params=params, data=data, files=files)
            except REST401Exception as e:
                # Reauthenticate and retry
                if authendpoint is not None and user is not None and password is not None:
                    authtoken, endpoint = authenticate(authendpoint, user, password)
                    response = callRESTApi(endpoint, basepath, resourcename, method='PUT', authtoken=authtoken, headers=headers, params=params, data=data, files=files)
                else:
                    raise
            # Remove splitfiles
            splitdir = getsplitdir(filename)
            shutil.rmtree(splitdir)
        else:
            # Simple single file upload
            basepath = imgbasepath
            # Upload file
            print('Uploading : ' + filename)
            resourcename = os.path.split(filename)[-1]
            with closing(open(filename, 'rb')) as f:
                response = callRESTApi(endpoint, basepath, resourcename, method='PUT', authtoken=authtoken, headers=headers, params=params, data=f, files=files)
            print('Uploaded : ' + filename)
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
