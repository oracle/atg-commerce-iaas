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

