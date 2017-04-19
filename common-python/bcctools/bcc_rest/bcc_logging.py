#!/usr/bin/python

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
__module__ = "bcc_logging"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import logging
import logging.handlers
import os
import time


loglevelname = 'info'
loglevel = logging.INFO
defaultloglevel = logging.INFO
loglevelmap = {'critical': logging.CRITICAL, 'error': logging.ERROR, 'warning': logging.WARNING, 'info': logging.INFO,
               'debug': logging.DEBUG}
logformat = '[UTC] %(asctime)-15s [%(process)s] (%(module)s-%(funcName)s-%(lineno)d) %(levelname)s: %(message)s'
logfilename = '/tmp/python-oc.log'


def getLogFormat():
    return logformat


def getLogFilename():
    global logfilename
    try:
        logfilename = os.getenv('OC_LOG_FILE', logfilename)
    except KeyError as e:
        logfilename = '/tmp/python-oc.log'
    return logfilename


def getLogLevel():
    global loglevel
    global loglevelname
    try:
        loglevelname = os.getenv('OC_LOG_LEVEL', loglevelname)
        loglevel = loglevelmap[loglevelname.lower()]
    except KeyError as e:
        loglevel = defaultloglevel
    return loglevel


def initLogging(name):
    logfilehandler = logging.handlers.RotatingFileHandler(getLogFilename(), maxBytes=10485760, backupCount=10)
    #logfilehandler = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_SYSLOG)
    logfilehandler.setLevel(getLogLevel())
    formatter = logging.Formatter(getLogFormat())
    formatter.converter = time.gmtime
    logfilehandler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(getLogLevel())
    logger.addHandler(logfilehandler)
    return logger

