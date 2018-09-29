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

from oc_provision_wrappers import commerce_setup_helper

import socket
import platform
import logging

logger = logging.getLogger(__name__)

json_key = 'WEBLOGIC_managed_servers'
common_key = 'WEBLOGIC_common'
service_name = "WebLogic Managed Server Scripts"


def create_managed_scripts(configData, full_path): 

    """
    Create start/stop scripts for managed servers
    """       
    if json_key in configData:
        jsonDataArray = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not install")
        return

    if common_key in configData:
        commonData = configData[common_key]
    else:
        logging.error(common_key + " config data missing from json. will not install")
        return    
                    
    logging.info("Updating... " + service_name)   
                 
    commonRequiredFields = ['middlewareHome', 'installOwner', 'installGroup', 'wl_domain', 'wl_adminHost', 'wl_adminHttpPort']
    commerce_setup_helper.check_required_fields(commonData, commonRequiredFields)   

    INSTALL_DIR = commonData['middlewareHome']
    INSTALL_OWNER = commonData['installOwner']
    INSTALL_GROUP = commonData['installGroup']
    WL_DOMAIN_NAME = commonData['wl_domain']
    WL_ADMIN_HOST = commonData['wl_adminHost']
    WL_ADMIN_HTTP_PORT = commonData['wl_adminHttpPort']
                
    WL_DOMAIN_HOME = INSTALL_DIR + '/user_projects/domains/' + WL_DOMAIN_NAME
    ADMIN_URL = WL_ADMIN_HOST + ":" + WL_ADMIN_HTTP_PORT

    if (platform.system() == 'SunOS'):
        startStopPath = "/startStopScripts/solaris/bootScripts/"
    else:
        startStopPath = "/startStopScripts/bootScripts/"
        
    for jsonData in jsonDataArray:
                
        requiredFields = ['managedServerName', 'managedServerHost', 'wl_startManaged_onBoot']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
        
        WL_SERVER_NAME = jsonData['managedServerName']
        WL_SERVER_HOST = jsonData['managedServerHost']
        WL_SERVER_BOOT = jsonData['wl_startManaged_onBoot']        
        
        # copy start/stop script
        WL_DOMAIN_HOME = INSTALL_DIR + '/user_projects/domains/' + WL_DOMAIN_NAME
        wlScript_replacements = {'WL_DOMAIN_HOME':WL_DOMAIN_HOME, "WL_PROCESS_OWNER":INSTALL_OWNER, "INSTANCE_NAME":WL_SERVER_NAME, "ADMIN_URL":ADMIN_URL}


        HOSTNAME_FROM_MACHINE = commerce_setup_helper.find_host_from_machine(WL_SERVER_HOST, configData, full_path)
                              

        logging.info("Done copying the start/stop scripts........." + HOSTNAME_FROM_MACHINE)        
                # try to get the fqdn
        FQDN = socket.getfqdn()
        logging.info("FQDN is:  " + FQDN)
        if (FQDN is not None):
            HOSTNAME = FQDN.split(".")[0]
            logging.info("HOSTNAME is : " + HOSTNAME)
            logging.info("WL_SERVER_HOST is : " + WL_SERVER_HOST)
            if (FQDN == HOSTNAME_FROM_MACHINE or HOSTNAME == HOSTNAME_FROM_MACHINE):
                SCRIPT_NAME = 'weblogicManaged-' + WL_SERVER_NAME
                logging.info('Generating startup script for server ' + WL_SERVER_NAME)
                commerce_setup_helper.copy_start_script(WL_SERVER_BOOT, full_path + startStopPath + 'weblogicManaged.master', wlScript_replacements, SCRIPT_NAME)
                
                # make the path to the log dir, or first server start will fail with scripts
                logging.info('Generating log dir for server ' + WL_SERVER_NAME)
                SERVER_LOG_PATH = WL_DOMAIN_HOME + '/servers/' + WL_SERVER_NAME + '/logs'
                commerce_setup_helper.mkdir_with_perms(SERVER_LOG_PATH, INSTALL_OWNER, INSTALL_GROUP)
                
                # fire up the instance 
                logging.info('Starting up instance ' + WL_SERVER_NAME)
                startCmd = "/etc/init.d/" + SCRIPT_NAME
                commerce_setup_helper.exec_cmd(startCmd + " restart")                   
            else:
                logging.error("Cannot determine hostname, fqdn or wl_server_host.......")

        else:
            logging.error("Cannot determine hostname. Cannot create startup script")
        
