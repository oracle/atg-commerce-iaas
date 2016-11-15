import getopt
import getopt
import os
import sys

from java.lang import System


#===============================
# Input Values Validation Section
#===============================
if __name__ == '__main__' or __name__ == 'main':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:a:m:h:", ["username=", "password=", "adminUrl=", "machineName=", "hostAddress="])

    except getopt.GetoptError, err:
        print str(err)
        usage()

    username = ''
    password = ''
    adminUrl = ''
    machineName = ''
    hostAddress = ''

    for opt, arg in opts:
        if opt == "-u":
            username = arg
        elif opt == "-p":
            password = arg
        elif opt == "-a":
            adminUrl = arg
        elif opt == "-m":
            machineName = arg
        elif opt == "-h":
            hostAddress = arg                                  

    if username == "":
        print "Missing \"-u username\" parameter.\n"
        usage()
    elif password == "":
        print "Missing \"-p password\" parameter.\n"
        usage()
    elif adminUrl == "":
        print "Missing \"-a adminUrl\" parameter.\n"
        usage()
    elif machineName == "":
        print "Missing \"-n machineName\" parameter.\n"
        usage()
    elif hostAddress == "":
        print "Missing \"-h hostAddress\" parameter.\n"
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
# Create machine
###################################################################
def create_machine():
    try:
        print 'Creating machine...';
        edit();
        startEdit();

        cd('/')
         
        # create a unix machine
        myMachine = cmo.createUnixMachine(machineName)
                  
        # set the nodemanager settings, again that match the settings set up in 
        # the create domain script
        myMachine.getNodeManager().setNMType('ssl')
        myMachine.getNodeManager().setListenAddress(hostAddress)
         
        # save and activate the changes
        save()
        activate(block="true")

    except:
        print 'Exception while creating machine';
        dumpStack();
        cancelEdit('y')
        exit();


connectToDomain();
create_machine();
print 'Done creating machine ' + machineName
exit();    


