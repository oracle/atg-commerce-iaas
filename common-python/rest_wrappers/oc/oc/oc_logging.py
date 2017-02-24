#!/usr/bin/python
# Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved.


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
__module__ = "oc_logging"
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

