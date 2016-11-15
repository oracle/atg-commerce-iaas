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
__module__ = "oc_exceptions"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


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



