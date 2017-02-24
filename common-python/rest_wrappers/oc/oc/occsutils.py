#
# Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved.


"""Provide Module Description
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Andrew Hopkinson (Oracle Cloud Solutions A-Team)"
__copyright__ = "Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "occsutils"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import getpass
import json
import requests

from oc_logging import initLogging

from oc_exceptions import RESTException
from oc_exceptions import OCAlreadyStarted
from oc_exceptions import OCAlreadyStopped
from oc_exceptions import REST401Exception
from oc_exceptions import OCActionNotPermitted
from oc_exceptions import OCAuthorisationTokenInvalid
from oc_exceptions import REST404Exception
from oc_exceptions import OCObjectDoesNotExist
from oc_exceptions import REST409Exception
from oc_exceptions import OCObjectAlreadyExists


def showVersionHistory():
    print('')
    print('##########################################################################################')
    print('## Version    Date         Change')
    print('## =======    ==========   ===============================================================')
    print('##')
    print('## 1.0.0.0    04/03/2016   1. Initial release.')
    print('##')
    print('##########################################################################################')
    print('')
    return


mylogger = initLogging(__name__)
httpSession = None
restEndpoint = None


def clearHTTPSession():
    global httpSession
    httpSession = None
    return


def getHTTPSession():
    global httpSession
    headers = {'Accept': 'application/oracle-compute-v3+json', 'Accept-Encoding': 'gzip;q=1.0, identity; q=0.5',
               'Content-Type': 'application/oracle-compute-v3+json'}
    if httpSession is None:
        httpSession = requests.Session()
        httpSession.headers.update(headers)
    return httpSession


def getRESTEndpoint():
    return restEndpoint


def setRESTEndpoint(url):
    global restEndpoint
    restEndpoint = url
    return


def callRESTApi(endpoint, basepath, resourcename='', data=None, method='GET', params=None, cookie=None, **kwargs):
    response = {}
    client = getHTTPSession()
    if cookie is not None:
        client.cookies['nimbula'] = cookie
    url = generateRESTurl(endpoint, basepath, resourcename)
    #print('url     : ' + str(url))
    #print('params  : ' + str(params))
    #print('data    : ' + str(data))
    #print('headers : ' + str(headers))
    requests.packages.urllib3.disable_warnings()
    if method.upper() == 'GET':
        response = client.get(url, params=params, verify=False)
    elif method.upper() == 'POST':
        response = client.post(url, data=json.dumps(data), verify=False)
    elif method.upper() == 'PUT':
        response = client.put(url, params=params, verify=False)
    elif method.upper() == 'DELETE':
        response = client.delete(url, verify=False)
    # Clean because it seems reusing the session fails
    clearHTTPSession()
    #print('response headers : ' + str(response.headers))
    #print('response status  : ' + str(response.status_code))
    #print('response text    : ' + str(response.text))

    # Check response and raise exception if necessary
    mylogger.debug("Response ({0:d}) : {1:s}".format(response.status_code, response.text))
    if response.status_code == 401:
        mylogger.warn("Response ({0:d}) : {1:s}".format(response.status_code, response.text))
        # Attempt to convert generic response to meaningful Exception.
        if 'is not permitted to perform' in response.text:
            raise OCActionNotPermitted(str(response.text))
        elif 'Authorization token is invalid' in response.text:
            raise OCAuthorisationTokenInvalid(str(response.text))
        else:
            raise REST401Exception('{0:s} : {1:s}'.format(str(response.status_code), str(response.text)))
    elif response.status_code == 404:
        mylogger.warn("Response ({0:d}) : {1:s}".format(response.status_code, response.text))
        if 'not found' in response.text:
            raise OCObjectDoesNotExist(str(response.text))
        elif 'does not exist' in response.text:
            raise OCObjectDoesNotExist(str(response.text))
        else:
            raise REST404Exception('{0:s} : {1:s}'.format(str(response.status_code), str(response.text)))
    elif response.status_code == 409:
        mylogger.warn("Response ({0:d}) : {1:s}".format(response.status_code, response.text))
        if 'already exists' in response.text:
            raise OCObjectAlreadyExists(str(response.text))
        elif 'does not exist' in response.text:
            raise OCObjectDoesNotExist(str(response.text))
        else:
            raise REST409Exception('{0:s} : {1:s}'.format(str(response.status_code), str(response.text)))
    elif response.status_code >= 400 and response.status_code < 600:
        mylogger.warn("Response ({0:d}) : {1:s}".format(response.status_code, response.text))
        if 'is already started' in response.text:
            raise OCAlreadyStarted(str(response.text))
        elif 'is already stopped' in response.text:
            raise OCAlreadyStopped(str(response.text))
        else:
            raise RESTException('{0:s} : {1:s}'.format(str(response.status_code), str(response.text)))

    return response


def generateRESTurl(endpoint, basepath, resourcename='', **kwargs):
    url = str(endpoint).strip('/') + '/'
    if basepath is not None and basepath != '':
        url += str(basepath).strip('/') + '/'
        if resourcename is not None and resourcename != '':
            url += str(resourcename).strip('/') + '/'
    return url


# Get password
def getPassword(user=None, prompt=None, **kwargs):
    if prompt is None:
        if user is not None:
            prompt = 'Please enter password for user ' + user + ' : '
        else:
            prompt = 'Please enter password : '
    password = getpass.getpass(prompt)
    return password


def printJSON(jsonObj, sortKeys=True, indent=2, **kwargs):
    if jsonObj is not None:
        print(json.dumps(jsonObj, indent=indent, separators=(',', ': ')))
    return
