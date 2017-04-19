#

# The MIT License (MIT)
#
# Copyright (c) 2017 Oracle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (Oracle A-Team)"
__copyright__ = "Copyright (c) 2017 Oracle"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "authenticate"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import getpass
import json
import requests
import ast

from bcc_logging import initLogging

from bcc_exceptions import RESTException 
from bcc_exceptions import REST401Exception
from bcc_exceptions import REST404Exception
from bcc_exceptions import REST409Exception


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
    #headers = {'Accept': 'application/oracle-compute-v3+json', 'Accept-Encoding': 'gzip;q=1.0, identity; q=0.5', 'Content-Type': 'application/oracle-compute-v3+json'}
    headers = {'Content-Type': 'application/json'}
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
    
    if data is None:
        data = {}

    if cookie is not None:
        dictData = dict(ast.literal_eval(cookie.strip()))
        if 'JSESSIONID' in dictData:
            client.cookies['JSESSIONID'] = dictData['JSESSIONID']
        # we need to pass dynSessConf no matter what
        if '_dynSessConf' in dictData:
            data['_dynSessConf'] = dictData['_dynSessConf']
            

    #jsonData = json.dumps(data)
    #print jsonData
    url = generateRESTurl(endpoint, basepath, resourcename)
    #print('url     : ' + str(url))
    #print('params  : ' + str(params))
    #print('data    : ' + str(data))
    #print('headers : ' + str(client.headers))
    #print ('cookies : ' + str(client.cookies))
    requests.packages.urllib3.disable_warnings()
    if method.upper() == 'GET':
        response = client.get(url, params=params, verify=False)
    elif method.upper() == 'POST':
        response = client.post(url, data=json.dumps(data), verify=False)
        #print "************************"
        #print response.text        
        #print "************************"
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
        raise REST401Exception('{0:s} : {1:s}'.format(str(response.status_code), str(response.text)))
    elif response.status_code == 404:
        mylogger.warn("Response ({0:d}) : {1:s}".format(response.status_code, response.text))
        raise REST404Exception('{0:s} : {1:s}'.format(str(response.status_code), str(response.text)))
    elif response.status_code == 409:
        mylogger.warn("Response ({0:d}) : {1:s}".format(response.status_code, response.text))
        raise REST409Exception('{0:s} : {1:s}'.format(str(response.status_code), str(response.text)))
    elif response.status_code >= 400 and response.status_code < 600:
        mylogger.warn("Response ({0:d}) : {1:s}".format(response.status_code, response.text))
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
