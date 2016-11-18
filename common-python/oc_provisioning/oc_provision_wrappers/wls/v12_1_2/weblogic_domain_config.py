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

import platform
import time

from oc_provision_wrappers import commerce_setup_helper
import weblogic_packer
import os


json_key = 'WEBLOGIC_domain_setup'
common_key = 'WEBLOGIC_common'
service_name = "WebLogic Domain"

def create_wl_domain(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        print json_key + " config data missing from json. will not install"
        return

    if common_key in configData:
        commonData = configData[common_key]
    else:
        print common_key + " config data missing from json. will not install"
        return   
    
    print "Creating " + service_name 
     
    response_files_path = full_path + "/responseFiles/wls-12.1.2"
                      
    commonRequiredFields = ['middlewareHome', 'installOwner', 'wl_domain', 'wl_adminHttpPort', 'wl_adminHttpsPort', 'wl_adminPassword']
    commerce_setup_helper.check_required_fields(commonData, commonRequiredFields)
    
    requiredFields = ['wl_startAdmin_onBoot', 'wl_startNodemgr_onBoot']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)    

    INSTALL_DIR = commonData['middlewareHome']
    INSTALL_OWNER = commonData['installOwner']
    WL_DOMAIN_NAME = commonData['wl_domain']
    WL_ADMIN_HTTP_PORT = commonData['wl_adminHttpPort']
    WL_ADMIN_HTTPS_PORT = commonData['wl_adminHttpsPort']
    WL_ADMIN_PW = commonData['wl_adminPassword']
    WL_ADMIN_BOOT = jsonData['wl_startAdmin_onBoot']
    WL_NODE_BOOT = jsonData['wl_startNodemgr_onBoot']

    WL_MACHINES = add_machines(configData, full_path)
    WL_MANAGED_SERVERS = add_managed_servers(configData, full_path)
    
    wlst_path = INSTALL_DIR + "/wlserver/common/bin/wlst.sh"
    
    if not os.path.exists(wlst_path):
        print "Binary " + wlst_path + " does not exist - will not install"
        return False        
    
    wl_replacements = {'INSTALL_DIR':INSTALL_DIR, 'WL_DOMAIN_NAME':WL_DOMAIN_NAME, 'WL_ADMIN_HTTP_PORT':WL_ADMIN_HTTP_PORT, 'WL_ADMIN_HTTPS_PORT':WL_ADMIN_HTTPS_PORT, 'WL_ADMIN_PW':WL_ADMIN_PW, 'WL_MANAGED_SERVERS':WL_MANAGED_SERVERS, 'WL_MACHINES':WL_MACHINES}
    commerce_setup_helper.substitute_file_fields(response_files_path + '/basicWLSDomain.py.master', response_files_path + '/basicWLSDomain.py', wl_replacements)

    domainCmd = "\""
    
    JAVA_RAND = ""
    # if linux/Solaris, change random, This is faster in some implementations.
    if (platform.system() == "SunOS"):
        JAVA_RAND = "-Djava.security.egd=file:///dev/urandom"
    else:
        JAVA_RAND = "-Djava.security.egd=file:/dev/./urandom"
        
    # create wl domain CONFIG_JVM_ARGS
    domainCmd += "export CONFIG_JVM_ARGS='" + JAVA_RAND + "'; "
    domainCmd += wlst_path + " " + response_files_path + "/basicWLSDomain.py " + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, domainCmd)  
   
    if (platform.system() == 'SunOS'):
        startStopPath = "/startStopScripts/solaris/bootScripts/"
    else:
        startStopPath = "/startStopScripts/bootScripts/"
        
    # copy start/stop script
    WL_DOMAIN_HOME = INSTALL_DIR + '/user_projects/domains/' + WL_DOMAIN_NAME
    wlScript_replacements = {'WL_DOMAIN_HOME':WL_DOMAIN_HOME, "WL_PROCESS_OWNER":INSTALL_OWNER}
    commerce_setup_helper.copy_start_script(WL_ADMIN_BOOT, full_path + startStopPath + 'weblogicAdmin.master', wlScript_replacements)
    commerce_setup_helper.copy_start_script(WL_NODE_BOOT, full_path + startStopPath + 'weblogicNodemgr.master', wlScript_replacements)
    
    # pack the domain for managed servers
    weblogic_packer.pack_domain(configData, full_path)
    
    # fire up the admin server and nodemgr 
    startWLCmd = "/etc/init.d/weblogicAdmin"
    commerce_setup_helper.exec_cmd(startWLCmd + " start")
    startNodeCmd = "/etc/init.d/weblogicNodemgr"
    commerce_setup_helper.exec_cmd(startNodeCmd + " start")
    
    # give admin server time to finish starting
    sleepTime = 60
    time.sleep(sleepTime)
    
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "# echo 'WebLogic Admin start/stop script: '" + startWLCmd + "\n")    
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "# echo 'WebLogic NodeManager start/stop script: '" + startNodeCmd + "\n")   
    
def add_managed_servers(configData, full_path):
    
    managed_key = "WEBLOGIC_managed_servers"
    if managed_key in configData:
        jsonDataArray = configData[managed_key]
    else:
        print managed_key + " missing from json. will not add managed servers"
        return ''
    
    print "adding managed servers"
    serverData = ''
    
    for jsonData in jsonDataArray:             
        requiredFields = ['managedServerName', 'managedServerHttpPort', 'managedServerHost']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    
        WL_SERVER_NAME = jsonData['managedServerName']
        WL_SERVER_PORT = jsonData['managedServerHttpPort']
        WL_SERVER_HOST = jsonData['managedServerHost']
        
        serverData += "cd('/') \n"
        serverData += "create('" + WL_SERVER_NAME + "', 'Server')\n"
        serverData += "cd('Server/" + WL_SERVER_NAME + "')\n"
        serverData += "set('ListenPort', " + WL_SERVER_PORT + ")\n"
        serverData += "set('ListenAddress', '" + WL_SERVER_HOST + "')\n"
        serverData += "cd('/') \n"
        serverData += "assign('Server', '" + WL_SERVER_NAME + "', 'Machine','" + WL_SERVER_HOST + "') \n"
                
    return serverData
        
def add_machines(configData, full_path):
    
    machine_key = "WEBLOGIC_machines"
    if machine_key in configData:
        jsonDataArray = configData[machine_key]
    else:
        print machine_key + " missing from json. will not add machines"
        return ''
    
    print "adding machines"
    machineData = ''
    
    for jsonData in jsonDataArray:             
        requiredFields = ['machineName', 'machineAddress']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    
        WL_MACHINE_NAME = jsonData['machineName']
        WL_MACHINE_ADDR = jsonData['machineAddress']           
        
        machineData += "cd('/') \n"
        machineData += "create('" + WL_MACHINE_NAME + "', 'UnixMachine')\n"
        machineData += "cd('Machines/" + WL_MACHINE_NAME + "')\n"
        machineData += "create('" + WL_MACHINE_NAME + "', 'NodeManager')\n"
        machineData += "cd('NodeManager/" + WL_MACHINE_NAME + "')\n"
        machineData += "set('NMType', 'SSL') \n"
        machineData += "set('ListenAddress', '" + WL_MACHINE_ADDR + "')\n"
        
    return machineData    

