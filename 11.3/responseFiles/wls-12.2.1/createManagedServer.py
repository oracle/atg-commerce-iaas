# The MIT License (MIT)
#
# Copyright (c) 2018 Oracle
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
__copyright__ = "Copyright (c) 2018  Oracle and/or its affiliates. All rights reserved."
__credits__ ="Hadi Javaherian (Oracle IaaS and App Dev Team)"
__version__ = "1.0.0.1"
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
        opts, args = getopt.getopt(sys.argv[1:], "u:p:a:n:h:m:", ["username=", "password=", "adminUrl=", "nserverName=", "hserverPort=", "machine="])

    except getopt.GetoptError, err:
        print str(err)
        usage()

    username = ''
    password = ''
    adminUrl = ''
    nserverName = ''
    hserverPort = ''
    machine = ''

    for opt, arg in opts:
        if opt == "-u":
            username = arg
        elif opt == "-p":
            password = arg
        elif opt == "-a":
            adminUrl = arg
        elif opt == "-n":
            nserverName = arg
            print "nserverName is " + nserverName
        elif opt == "-h":
            hserverPort = arg
        elif opt == "-m":
            machine = arg                                    

    if username == "":
        print "Missing \"-u username\" parameter.\n"
        usage()
    elif password == "":
        print "Missing \"-p password\" parameter.\n"
        usage()
    elif adminUrl == "":
        print "Missing \"-a adminUrl\" parameter.\n"
        usage()
    elif nserverName == "":
        print "Missing \"-n nserverName\" parameter.\n"
        usage()
    elif hserverPort == "":
        print "Missing \"-h hserverPort\" parameter.\n"
        usage()
    elif machine == "":
        print "Missing \"-m machine\" parameter.\n"
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
# Add managed server to machine
###################################################################
def addManagedServerToMachine(instance, machine, server):
    try:
        print 'adding instance to the machine...';

        edit();
        startEdit();

        cd('/Servers/' + instance)
        cmo.setListenAddress(server)
        cmo.setListenPortEnabled(true)
        cmo.setClientCertProxyEnabled(false)
        cmo.setJavaCompiler('javac')
        cmo.setMachine(getMBean('/Machines/' + machine))
        cmo.setCluster(None)

        cd('/Servers/' + instance + '/SSL/' + instance)

        cd('/Servers/bcc/ServerDiagnosticConfig/' + instance)

        save()
        activate(block="true")

    except:
        print 'Exception while adding machine to server';
        dumpStack();
        cancelEdit('y')
        exit();


#connectToDomain();
#createManagedServer();
print 'Done adding instance: ' + insance + ' to machine: ' + machine 
exit();

        
###################################################################
# Create managed server
###################################################################
def createManagedServer():
    try:
        print 'Creating managed server...';
        
        edit();
        startEdit();

        # create server
        cd('/')
        cmo.createServer(nserverName)
        # set listen address and port
        cd('/Servers/' + nserverName)
        cmo.setListenAddress('')
        cmo.setListenPort(int(hserverPort))
        cmo.setMachine(getMBean('/Machines/' + machine))
        cmo.setCluster(None)
        # cd('/Servers/' + name +'/SSL/'+ name )
        # cmo.setEnabled(true)
        # cmo.setListenPort(long(7104))
        
        # save and activate the changes
        save()
        activate(block="true")

    except:
        print 'Exception while creating managed server';
        dumpStack();
        cancelEdit('y')
        exit();


connectToDomain();
createManagedServer();
print 'Done creating managed server ' + nserverName
exit();

