# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (Oracle A-Team)"
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import getopt
import os
import sys

from java.lang import System


#===============================
# Input Values Validation Section
#===============================
if __name__ == '__main__' or __name__ == 'main':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:a:j:", ["username=", "password=", "adminUrl=", "jtaTimeout="])

    except getopt.GetoptError, err:
        print str(err)
        usage()

    username = ''
    password = ''
    adminUrl = ''
    jtaTimeout = ''

    for opt, arg in opts:
        if opt == "-u":
            username = arg
        elif opt == "-p":
            password = arg
        elif opt == "-a":
            adminUrl = arg
        elif opt == "-j":
            jtaTimeout = arg
            
    if username == "":
        print "Missing \"-u username\" parameter.\n"
        usage()
    elif password == "":
        print "Missing \"-p password\" parameter.\n"
        usage()
    elif adminUrl == "":
        print "Missing \"-a adminUrl\" parameter.\n"
        usage()
    elif jtaTimeout == "":
        print "Missing \"-j jtaTimeout\" parameter.\n"
        usage()

###################################################################
# Connect to damain
###################################################################
def connectToDomain():
    try:
        if username != "":
            connect(username, password, adminUrl)
            print 'Successfully connected to the domain\n'

    except:
        print 'The domain is unreacheable. Please try again\n'
        exit()

###################################################################
# Setting Domain JTA Transaction timeout
###################################################################
def setDomainJTATimeout():
    try:
        print 'Setting Domain JTA Transaction timeout...';
        edit();
        startEdit();
        
        cd("/Servers")
        domainName = cmo.getName()
        
        cd('/JTA/' + domainName);
        
        # Maximum amount of time, in seconds, an active transaction
        # is allowed to be in the first phase of a transaction
        cmo.setTimeoutSeconds(int(jtaTimeout));
        
        save();
        activate();

    except:
        print 'Exception while setting Domain JTA Transaction timeout !';
        dumpStack();
        cancelEdit('y')
        exit();


connectToDomain();
setDomainJTATimeout();
exit();
