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

import distutils.core
import os

from oc_provision_wrappers import commerce_setup_helper  
 

def generate_atg_server_payers(configData, full_path):
    """
    Create ATG server layers based on the instance type
    """      
        
    # we need the server defs, and the path to the ATG install
    wl_managed_key = "WEBLOGIC_managed_servers"
    atg_key = "ATG_install"
    
    if wl_managed_key in configData:
        managedServerArray = configData[wl_managed_key]
    else:
        print wl_managed_key + " missing from json. will not create atg server layers"
        return ''

    if atg_key in configData:
        atgData = configData[atg_key]
    else:
        print atg_key + " missing from json. will not create atg server layers"
        return ''
    
    ATG_INSTALL_ROOT = atgData['dynamoRoot']
    ATG_CLUSTER_NAME = atgData['atg_clustername']
    ATG_SERVERS_HOME = ATG_INSTALL_ROOT + "/home/servers"
    
    print "Creating ATG Server layers"
    serverData = ''
    
    PROD_LOCK_PORTS_ARRAY = []
    PROD_LOCK_SERVERS_ARRAY = []
    
    # calculate lock server data first. We need this for all other instances
    for jsonData in managedServerArray:
        requiredFields = ['atgServerType']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
        ATG_SERVER_TYPE = jsonData['atgServerType']
        if (ATG_SERVER_TYPE == "lock"):
            PROD_LOCK_PORTS_ARRAY.append(jsonData['atgLockManPort'])
            PROD_LOCK_SERVERS_ARRAY.append(jsonData['managedServerHost'])

               
    
    for jsonData in managedServerArray:             
        requiredFields = ['managedServerName', 'managedServerHttpPort', 'managedServerHttpsPort', 'managedServerHost', 'atgServerType', 'atgRmiPort', 'atgFdPort', 'atgDrpPort']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    
        WL_SERVER_NAME = jsonData['managedServerName']
        WL_SERVER_HTTP_PORT = jsonData['managedServerHttpPort']
        WL_SERVER_HTTPS_PORT = jsonData['managedServerHttpsPort']
        WL_SERVER_HOST = jsonData['managedServerHost']
        ATG_SERVER_TYPE = jsonData['atgServerType']
        ATG_RMI_PORT = jsonData['atgRmiPort']
        ATG_FD_PORT = jsonData['atgFdPort']
        ATG_DRP_PORT = jsonData['atgDrpPort']
        BCC_FILE_PORT = ""
        BCC_LOCK_PORT = ""
        ATG_LOCK_PORT = ""
        if 'bccFileSyncPort' in jsonData:
            BCC_FILE_PORT = jsonData['bccFileSyncPort']
        if 'bccLockPort' in jsonData:
            BCC_LOCK_PORT = jsonData['bccLockPort']            
        if 'atgLockManPort' in jsonData:                    
            ATG_LOCK_PORT = jsonData['atgLockManPort']
        
        PROD_LOCK_PORTS = ','.join(PROD_LOCK_PORTS_ARRAY)
        PROD_LOCK_SERVERS = ','.join(PROD_LOCK_SERVERS_ARRAY)
        
        server_layer_path = full_path + "/atg-server-layers/"
            
        distutils.dir_util.copy_tree(server_layer_path + ATG_SERVER_TYPE , ATG_SERVERS_HOME + "/" + WL_SERVER_NAME)
        string_replacements = {'ATG_DRP_PORT':ATG_DRP_PORT, 'ATG_RMI_PORT':ATG_RMI_PORT, 'ATG_FD_PORT':ATG_FD_PORT, 'ATG_HTTP_PORT':WL_SERVER_HTTP_PORT, \
                               'ATG_HTTPS_PORT':WL_SERVER_HTTPS_PORT, 'BCC_FILE_SYNC_PORT':BCC_FILE_PORT, 'BCC_LOCK_PORT':BCC_LOCK_PORT, \
                               'ATG_CLUSTER_NAME':ATG_CLUSTER_NAME, 'PROD_LOCK_PORTS':PROD_LOCK_PORTS, 'PROD_LOCK_SERVERS':PROD_LOCK_SERVERS}
        
        for dname, dirs, files in os.walk(ATG_SERVERS_HOME + "/" + WL_SERVER_NAME):
            for fname in files:
                fpath = os.path.join(dname, fname)
                commerce_setup_helper.substitute_file_fields_inplace(fpath, string_replacements)
        
                        
    return serverData
