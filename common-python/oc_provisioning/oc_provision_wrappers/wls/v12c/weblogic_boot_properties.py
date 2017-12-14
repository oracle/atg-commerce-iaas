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
__copyright__ = "Copyright (c) 2017  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from oc_provision_wrappers import commerce_setup_helper

import os
import socket
import logging

logger = logging.getLogger(__name__)

managed_key = 'WEBLOGIC_managed_servers'
common_key = 'WEBLOGIC_common'
service_name = "WebLogic Boot Properties"


def create_boot_properties(configData, full_path): 

    """
    Create boot.properties files for instances
    """       
    if managed_key in configData:
        jsonDataArray = configData[managed_key]
    else:
        logging.error(managed_key + " config data missing from json. will not install")
        return

    if common_key in configData:
        commonData = configData[common_key]
    else:
        logging.error(common_key + " config data missing from json. will not install")
        return    

    commonRequiredFields = ['middlewareHome', 'installOwner', 'installGroup', 'wl_domain']
    commerce_setup_helper.check_required_fields(commonData, commonRequiredFields)    

    INSTALL_DIR = commonData['middlewareHome']
    INSTALL_OWNER = commonData['installOwner']
    INSTALL_GROUP = commonData['installGroup']
    WL_DOMAIN_NAME = commonData['wl_domain']
    WL_ADMIN_USER = commonData['wl_adminUser']
    WL_ADMIN_PW = commonData['wl_adminPassword']
    
    SERVER_PATH = INSTALL_DIR + '/user_projects/domains/' + WL_DOMAIN_NAME + '/servers/'
    
    logging.info("Checking boot.properties setup")
    
    for jsonData in jsonDataArray:
        
        requiredFields = ['managedServerName', 'managedServerHost']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    
        WL_SERVER_NAME = jsonData['managedServerName']
        WL_SERVER_HOST = jsonData['managedServerHost']
        
        # try to get the fqdn
        FQDN = socket.getfqdn()
        if (FQDN is not None):
            HOSTNAME = FQDN.split(".")[0]
            if (FQDN == WL_SERVER_HOST or HOSTNAME == WL_SERVER_HOST):
                # make sure the base servers path exists
                if(os.path.exists(SERVER_PATH)):
                    # create the instance and security dir to write to boot file to
                    outpath = SERVER_PATH + WL_SERVER_NAME + "/security/"
                    commerce_setup_helper.mkdir_with_perms(outpath, INSTALL_OWNER, INSTALL_GROUP)
                    outfile = outpath + 'boot.properties'
                    outdata = open(outfile, 'w')
                    outdata.write('username=' + WL_ADMIN_USER + "\n")
                    outdata.write('password=' + WL_ADMIN_PW + "\n")
                    outdata.close()
                    # change the owner of boot.properties. should have been created by root
                    commerce_setup_helper.change_file_owner(outfile, INSTALL_OWNER, INSTALL_GROUP)
                    
                logging.info("Created boot.properties for " + WL_SERVER_NAME)
        else:
            logging.error("Cannot determine hostname. Cannot create boot.properties")
         
    