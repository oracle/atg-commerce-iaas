# The MIT License (MIT)
#
# Copyright (c) 2016 Oracle
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
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import ast
import json
import posixpath
import re
import urllib2


badCharRegex = re.compile(r'[/{}]', re.IGNORECASE)


_NO_DEFAULT = object()
           
def _get(path, default=_NO_DEFAULT):
    try:
        return urllib2.urlopen(path).read().strip()
    except urllib2.HTTPError as e:
        if e.code == 404 and default != _NO_DEFAULT:
            return default
        raise

def _test_dict(data):
    
    # if already a dict, just return
    if isinstance(data, dict):
        return
    
    return_list = []
    keys = data.split('\n')
    for k in keys:
        try:
            # if this is a dict, add to our list
            dictData = dict(ast.literal_eval(k.strip()))
            return_list.append(dictData)
        except:
            pass                

    return return_list

def _read_recursive(path, default=_NO_DEFAULT):
    # first read the data from the path
    raw_data = _get(path)

    # now test to see whether it is actually a list of keys
    # by attempting to read data from each one
    recursive_data = {}
    keys = raw_data.split('\n')
    for k in keys:
        badUrl = False
        if badCharRegex.search(k):
            badUrl = True     
        sub_path = posixpath.join(path, k)
        try:
            if not badUrl:
                sub_data = _read_recursive(sub_path)
                list_data = _test_dict(sub_data)
                if list_data:
                    recursive_data[k] = list_data
                else:
                    recursive_data[k] = sub_data                                
        except urllib2.HTTPError as e:
            if e.code != 404:
                raise

    # if any of the keys did return actual data
    if len(recursive_data.keys()) > 0:
        # set the other keys as being empty dicts
        for k in keys:
            if k not in recursive_data:
                recursive_data[k] = {}
        # then return it as a dict
        return recursive_data
    
    if raw_data == '' and default != _NO_DEFAULT:
        return default

    return raw_data    

def load_user_metadata(url, key):
    
    """
    Load user meta data from OPC
    """           
    metadata_url = posixpath.join(url, key)   
    configData = _read_recursive(metadata_url)  
    return configData

def load_os_user_metadata(url, key):
    
    """
    Load user meta data from OpenStack
    """           
    data = _get(url)
    jsonData = json.loads(data)
    if jsonData[key]:
        return jsonData[key]
    
    
