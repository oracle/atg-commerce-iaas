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
import shutil

from oc_provision_wrappers import commerce_setup_helper


json_key = 'WEBLOGIC_common'
service_name = "WebLogic Domain Pack"

def pack_domain(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        print json_key + " config data missing from json. will not install"
        return
                
    print "Packing... " + service_name                
    requiredFields = ['middlewareHome', 'installOwner', 'wl_domain']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    INSTALL_DIR = jsonData['middlewareHome']
    INSTALL_OWNER = jsonData['installOwner']
    WL_DOMAIN_NAME = jsonData['wl_domain']

        
    WL_DOMAIN_HOME = INSTALL_DIR + '/user_projects/domains/' + WL_DOMAIN_NAME
    DOMAIN_TEMPLATE_NAME = WL_DOMAIN_NAME + '-template.jar'
    DOMAIN_TEMPLATE_PATH = INSTALL_DIR + '/user_projects/domains/' + DOMAIN_TEMPLATE_NAME
    
    packCmd = "\"" + INSTALL_DIR + "/wlserver/common/bin/pack.sh -managed=true -domain=" + WL_DOMAIN_HOME + " -template=" + DOMAIN_TEMPLATE_PATH + " -template_name=" + WL_DOMAIN_NAME + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, packCmd)
    
    # put a copy of the packed domain in our special users homeDir
    templateUser = "wlinstall"
    homeDir = os.path.expanduser("~" + templateUser)
    if os.path.isdir(homeDir):
        shutil.copyfile(DOMAIN_TEMPLATE_PATH , homeDir + "/" + DOMAIN_TEMPLATE_NAME)
        os.chmod(homeDir + "/" + DOMAIN_TEMPLATE_NAME, 0644)
    else:
        print "user " + templateUser + " home dir not available. Will not copy packed domain" 
