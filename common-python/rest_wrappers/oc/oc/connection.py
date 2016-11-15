#
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
__module__ = "connection"
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


class RESTException(Exception):
    def __init__(self, *args):
        self.message = ''
        if len(args) > 0:
            self.message = args[0]
        Exception.__init__(self, *args)

    def __str__(self):
        return repr('REST Command Exception : ' + self.message)


class REST401Exception(Exception):
    def __init__(self, *args):
        self.message = ''
        if len(args) > 0:
            self.message = args[0]
        Exception.__init__(self, *args)

    def __str__(self):
        return repr('REST 401 Exception : ' + self.message)


class REST409Exception(Exception):
    def __init__(self, *args):
        self.message = ''
        if len(args) > 0:
            self.message = args[0]
        Exception.__init__(self, *args)

    def __str__(self):
        return repr('REST 409 Exception : ' + self.message)


class Connection:

    def __init__(self, endpoint=None, user=None, password=None):
        self.endpoint = endpoint
        self.user = user
        self.password = password
        self.session = None
        self.response = None

    def authenticate(self):
        return

    def refreshtoken(self):
        return

    def clearsession(self):
        self.session = None
        return

    def getsession(self, headers={}):
        if self.session is None:
            self.session = requests.Session()
            self.session.headers.update(headers)
        return self.session

    def getendpoint(self):
        return self.endpoint

    def setendpoint(self, endpoint):
        self.endpoint = endpoint
        return

    def setuser(self, user):
        self.user = user
        return

    def setpassword(self, password):
        self.password = password
        return

    def get(self, url, headers={}, params={}, data={}, cookies=None):
        client = self.getsession(self, headers)
        self.response = client.get(url, params=params, verify=False)
        return self.response

    def post(self, url, headers={}, params={}, data={}, cookies=None):
        client = self.getsession(self, headers)
        self.response = client.post(url, data=json.dumps(data), verify=False)
        return self.response

    def put(self, url, headers={}, params={}, data={}, cookies=None):
        client = self.getsession(self, headers)
        self.response = client.put(url, params=params, verify=False)
        return self.response

    def delete(self, url, headers={}, params={}, data={}, cookies=None):
        client = self.getsession(self, headers)
        self.response = client.delete(url, verify=False)
        return self.response

    def checkresponse(self):
        # Check response and raise exception if necessary
        if self.response.status_code == 401:
            raise REST401Exception(str(self.response.text))
        elif self.response.status_code == 409:
            raise REST409Exception(str(self.response.text))
        elif self.response.status_code >= 400 and self.response.status_code < 600:
            raise RESTException(str(self.response.status_code) + ' - ' + str(self.response.text))
        return


class OCCSConnection(Connection):

    headers = {'Accept': 'application/oracle-compute-v3+json', 'Accept-Encoding': 'gzip;q=1.0, identity; q=0.5',
               'Content-Type': 'application/oracle-compute-v3+json'}

    def __init__(self, endpoint=None, user=None, password=None, cookie=None):
        Connection.__init__(endpoint, user, password)
        self.cookie = cookie

    def authenticate(self):
        self.clearsession()
        data = {"password": self.password, "user": self.user}
        basepath = '/authenticate/'
        resourcename = ''
        params = None
        self.callrest(self.endpoint, basepath, resourcename, data, 'POST', params)
        if self.response is not None and 'set-cookie' in self.response.headers:
            self.cookie = self.response.cookies['nimbula']
        else:
            self.cookie = ''
        return self.cookie

    def callrest(self, basepath='', resource='', method='GET', headers={}, params={}, data={}, files=None, **kwargs):
        if headers is not None:
            headers.update(self.headers)
        client = self.getsession(headers)
        if self.cookie is not None:
            client.cookies['nimbula'] = self.cookie
        url = self.generateresturl(basepath, resource)
        if method.upper() == 'GET':
            self.response = client.get(url, params=params, verify=False)
        elif method.upper() == 'POST':
            self.response = client.post(url, data=json.dumps(data), verify=False)
        elif method.upper() == 'PUT':
            self.response = client.put(url, params=params, verify=False)
        elif method.upper() == 'DELETE':
            self.response = client.delete(url, verify=False)
        self.checkresponse()
        return self.response


    def generateresturl(self, basepath='', resourcename='', **kwargs):
        url = str(self.endpoint).strip('/') + '/'
        if basepath is not None and basepath != '':
            url += str(basepath).strip('/') + '/'
            if resourcename is not None and resourcename != '':
                url += str(resourcename).strip('/') + '/'
        return url


class OSCSConnection(Connection):

    def __init__(self, endpoint=None, user=None, password=None, authtoken=None, storageurl=None):
        Connection.__init__(endpoint, user, password)
        self.authtoken = authtoken
        self.storageurl = storageurl

    def authenticate(self):
        self.clearsession()
        basepath = '/auth/v1.0/'
        resourcename = ''
        authtoken=None
        headers = {"X-Storage-Pass": self.password, "X-Storage-User": self.user}
        data = None
        params = None
        files = None
        response = self.callrest(self.endpoint, basepath, resourcename, method='GET', authtoken=authtoken, headers=headers, params=params, data=data, files=files)
        if response is not None and 'X-Auth-Token' in response.headers:
            self.authtoken = response.headers['X-Auth-Token']
        else:
            self.authtoken = ''
        if response is not None and 'X-Storage-Url' in response.headers:
            self.storageurl = response.headers['X-Storage-Url']
        else:
            self.storageurl = ''
        return self.authtoken, self.storageurl

    def callrest(self, basepath='', resource='', method='GET', headers={}, params={}, data={}, files=None, **kwargs):
        if headers is not None:
            headers.update(self.headers)
        client = self.getsession(headers)
        return self.response
