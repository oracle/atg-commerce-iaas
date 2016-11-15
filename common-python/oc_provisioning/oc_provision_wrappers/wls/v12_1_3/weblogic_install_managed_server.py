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

import os
import platform
import shutil
import time

from oc_provision_wrappers import commerce_setup_helper


json_key = 'WEBLOGIC_managed_server'
common_key = 'WEBLOGIC_common'
service_name = "WebLogic Domain Settings"


def unpack_domain(configData, full_path): 

    """
    Get domain template and unpack it for a new managed server setup
    """       
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
                    
    print "Unpacking... " + service_name   
                 
    commonRequiredFields = ['middlewareHome', 'installOwner', 'installGroup', 'wl_domain', 'wl_adminHost']
    commerce_setup_helper.check_required_fields(commonData, commonRequiredFields)
    
    requiredFields = ['wl_startNodemgr_onBoot']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)    

    INSTALL_DIR = commonData['middlewareHome']
    INSTALL_OWNER = commonData['installOwner']
    INSTALL_GROUP = commonData['installGroup']
    WL_DOMAIN_NAME = commonData['wl_domain']
    WL_ADMIN_HOST = commonData['wl_adminHost']
    WL_NODE_BOOT = jsonData['wl_startNodemgr_onBoot']
            
    WL_DOMAIN_HOME = INSTALL_DIR + '/user_projects/domains/' + WL_DOMAIN_NAME
    DOMAIN_TEMPLATE_NAME = WL_DOMAIN_NAME + '-template.jar'
    DOMAIN_TEMPLATE_PATH = INSTALL_DIR + '/user_projects/domains/' + DOMAIN_TEMPLATE_NAME
    
    if not os.path.isfile(DOMAIN_TEMPLATE_PATH):
        print "domain template not found. Try to get it"
        # make the install tree with correct owner if needed
        commerce_setup_helper.mkdir_with_perms(WL_DOMAIN_HOME, INSTALL_OWNER, INSTALL_GROUP)        
        retrieve_domain_template(DOMAIN_TEMPLATE_NAME, DOMAIN_TEMPLATE_PATH, WL_ADMIN_HOST)
        
    
    unpackCmd = "\"" + INSTALL_DIR + "/wlserver/common/bin/unpack.sh -domain=" + WL_DOMAIN_HOME + " -template=" + WL_DOMAIN_HOME + "-template.jar\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, unpackCmd)
    
    # copy start/stop script
    WL_DOMAIN_HOME = INSTALL_DIR + '/user_projects/domains/' + WL_DOMAIN_NAME

    if (platform.system() == 'SunOS'):
        startStopPath = "/startStopScripts/solaris/bootScripts/"
    else:
        startStopPath = "/startStopScripts/bootScripts/"
    # copy start/stop script
    WL_DOMAIN_HOME = INSTALL_DIR + '/user_projects/domains/' + WL_DOMAIN_NAME
    wlScript_replacements = {'WL_DOMAIN_HOME':WL_DOMAIN_HOME, "WL_PROCESS_OWNER":INSTALL_OWNER}
    commerce_setup_helper.copy_start_script(WL_NODE_BOOT, full_path + startStopPath + 'weblogicNodemgr.master', wlScript_replacements)
    
    # fire up the nodemgr 
    startNodeCmd = "/etc/init.d/weblogicNodemgr"
    commerce_setup_helper.exec_cmd(startNodeCmd + " start")      
    
def retrieve_domain_template(DOMAIN_TEMPLATE_NAME, DOMAIN_TEMPLATE_PATH, WL_ADMIN_HOST):
    print "Try to get domain template"
    
    templateUser = "wlinstall"
    
    copyCmd = "\"" + "scp -oStrictHostKeyChecking=no " + WL_ADMIN_HOST + ":" + DOMAIN_TEMPLATE_NAME + " ." + "\""
    
    # try this X number of times
    loops = 15
    sleepTime = 60
    
    for _count in xrange(loops):
        returnCode = commerce_setup_helper.exec_as_user(templateUser, copyCmd)
        print "scp returned " + str(returnCode)
        if returnCode == 0:
            break
        time.sleep(sleepTime)
        
    homeDir = os.path.expanduser("~" + templateUser)
    shutil.copyfile(homeDir + "/" + DOMAIN_TEMPLATE_NAME, DOMAIN_TEMPLATE_PATH)
    os.chmod(homeDir + "/" + DOMAIN_TEMPLATE_NAME, 0644)        
    
    
