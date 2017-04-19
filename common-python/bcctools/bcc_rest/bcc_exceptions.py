
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

"""Provide Module Description
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Andrew Hopkinson (Oracle Cloud Solutions A-Team)"
__copyright__ = "Copyright (c) 2017 Oracle"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "bcc_exceptions"
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

class REST404Exception(Exception):
    def __init__(self, *args):
        self.message = ''
        if len(args) > 0:
            self.message = args[0]
        Exception.__init__(self, *args)

    def __str__(self):
        return repr('REST 404 Exception : ' + self.message)

class REST409Exception(Exception):
    def __init__(self, *args):
        self.message = ''
        if len(args) > 0:
            self.message = args[0]
        Exception.__init__(self, *args)

    def __str__(self):
        return repr('REST 409 Exception : ' + self.message)
