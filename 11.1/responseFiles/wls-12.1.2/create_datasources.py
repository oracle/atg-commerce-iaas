# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (Oracle A-Team)"
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import getopt
import sys            

def usage():
    print "\n please check your input parameters. Something went wrong. \n"
    exit()
           
###################################################################
# Connect to damain
###################################################################
def connectToDomain():
    try:
        if wlusername != "":
            connect(wlusername, wlpassword, adminUrl)
            print 'Successfully connected to the domain\n'

    except:
        print 'The domain is unreacheable. Please try again\n'
        exit()


###################################################################
# Setting Domain JTA Transaction timeout
###################################################################
def create_ds():

    # dsJNDIName = "jdbc/testDS"
    # dsURL = "jdbc:oracle:thin:@localhost:1521:orcl"
    # dsDriver = "oracle.jdbc.xa.client.OracleXADataSource"
    # dsUsername = "atgcore"
    # dsPassword = "password1"
    # dsTargetType = configProps.get("ds.target.type")
    # dsTargetName = 'test1'
    
    # dump vars
    if (debug):
        print 'adminURL=', adminUrl
        print 'dsName=', dsName
        print 'dsJNDIName=', dsJNDIName
        print 'dsURL=', dsURL
        print 'dsDriver=', dsDriver
        print 'dsUsername=', dsUsername
        print 'dsPassword=', dsPassword
        print 'dsTargetType=', dsTargetType
        print 'dsTargetNames=', dsTargetNames
    
    edit()
    startEdit()
    
    # Create data source.
    cd('/')
    cmo.createJDBCSystemResource(dsName)
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
    cmo.setName(dsName)
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
    set('JNDINames', jarray.array([String(dsName)], String))
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName)
    cmo.setUrl(dsURL)
    cmo.setDriverName(dsDriver)
    set('Password', dsPassword)
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
    cmo.setMaxCapacity(int(dsMaxCapacity))
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName)
    cmo.createProperty('user')
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
    cmo.setValue(dsUsername)
    
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
    cmo.setGlobalTransactionsProtocol('TwoPhaseCommit')
    
    cd('/SystemResources/' + dsName)
    targets = dsTargetNames.split(',')
    targetObject = []
    for target in targets:
        targetObject.append(ObjectName('com.bea:Name=' + target + ',Type=Server'))
        
    set('Targets', jarray.array(targetObject, ObjectName))
    
    save()
    activate()

#===============================
# Input Values Validation Section
#===============================       
try:
    opts, args = getopt.getopt(sys.argv[1:], '', ["wlusername=", "wlpassword=", "adminUrl=", "dsName=", "dsJNDIName=", "dsURL=",
                                                  "dsDriver=", "dsUsername=", "dsPassword=", "dsTargetNames=", "dsMaxCapacity=", "debug=" ])

except getopt.GetoptError, err:
    print str(err)
    usage()

wlusername = ''
wlpassword = ''
adminUrl = ''
dsName = ''
dsJNDIName = ''
dsURL = ''
dsDriver = ''
dsUsername = ''
dsPassword = ''
dsTargetNames = ''
dsMaxCapacity = ''
dsTargetType = 'Server'
debug = ''

for opt, arg in opts:
    if opt == "--wlusername":
        wlusername = arg
    elif opt == "--wlpassword":
        wlpassword = arg
    elif opt == "--adminUrl":
        adminUrl = arg
    elif opt == "--dsName":
        dsName = arg
    elif opt == "--dsJNDIName":
        dsJNDIName = arg
    elif opt == "--dsURL":
        dsURL = arg
    elif opt == "--dsDriver":
        dsDriver = arg
    elif opt == "--dsUsername":
        dsUsername = arg
    elif opt == "--dsPassword":
        dsPassword = arg
    elif opt == "--dsTargetNames":
        dsTargetNames = arg
    elif opt == "--dsMaxCapacity":
        dsMaxCapacity = arg 
    elif opt == "--debug":
        debug = arg               
                                            
if wlusername == "":
    print "Missing \" wlusername\" parameter.\n"
    usage()
elif wlpassword == "":
    print "Missing \" password\" parameter.\n"
    usage()
elif adminUrl == "":
    print "Missing \" adminUrl\" parameter.\n"
    usage()
elif dsName == "":
    print "Missing \" dsName\" parameter.\n"
    usage()
if dsJNDIName == "":
    print "Missing \" dsJNDIName\" parameter.\n"
    usage()
elif dsURL == "":
    print "Missing \" dsURL\" parameter.\n"
    usage()
elif dsDriver == "":
    print "Missing \" dsDriver\" parameter.\n"
    usage()
elif dsUsername == "":
    print "Missing \" dsUsername\" parameter.\n"
    usage()       
elif dsPassword == "":
    print "Missing \" dsPassword\" parameter.\n"
    usage()
elif dsTargetNames == "":
    print "Missing \" dsTargetNames\" parameter.\n"
    usage()   
elif dsMaxCapacity == "":
    print "Missing \" dsMaxCapacity\" parameter.\n"
    usage()   

#===============================
# Login and create DS
#===============================  
connectToDomain();
create_ds();
exit();   

