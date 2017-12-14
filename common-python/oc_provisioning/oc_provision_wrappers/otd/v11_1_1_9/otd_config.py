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

from oc_provision_wrappers import commerce_setup_helper
import platform
import logging

logger = logging.getLogger(__name__)

json_key = 'OTD_config'
service_name = "OTD_Configuration"
installer_key = 'otd'


# OTD 11.1.1.9
def config_otd(configData, full_path): 
    
    if json_key in configData:
        jsonArray = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not install")
        return
    
    # get info from json on what version we are installing
    installer_config_data = commerce_setup_helper.get_installer_config_data(configData, full_path, installer_key)
    
    if (not installer_config_data):
        return False
    
    service_version = installer_config_data['service_version'] 
        
    logging.info("installing " + service_name)    
    
    response_files_path = full_path + "/responseFiles/" + service_version 
            
    for otdData in jsonArray:
        requiredFields = ['configName', 'installDir', 'adminUser', 'adminPassword', 'installOwner', 'virtualServerName', 'virtualServerPort', 'originServers', 'originPoolName',
                          'originServerType', 'loadDistribution', 'healthCheckUrl', 'healthCheckMethod', 'instanceHostname']
        commerce_setup_helper.check_required_fields(otdData, requiredFields)
        CONFIG_NAME = otdData['configName']
        INSTALL_DIR = otdData['installDir']
        INSTALL_OWNER = otdData['installOwner']
        ADMIN_USER = otdData['adminUser']
        ADMIN_PASSWORD = otdData['adminPassword']
        VSERVER_NAME = otdData['virtualServerName']
        VSERVER_PORT = otdData['virtualServerPort']
        OSERVERS = otdData['originServers']
        OPOOL_NAME = otdData['originPoolName']
        OSERVER_TYPE = otdData['originServerType']
        LOAD_ALG = otdData['loadDistribution']
        HEALTH_CHECK_URL = otdData['healthCheckUrl']
        HEALTH_CHECK_METHOD = otdData['healthCheckMethod']
        INSTANCE_HOME = otdData['instanceHome']
        INSTANCE_HOST = otdData['instanceHostname']
        OTD_START_BOOT = otdData['otd_start_onBoot']
        
        TADM_COMMAND = INSTALL_DIR + "/bin/tadm"
        otdPassword_replacements = {'TADM_ADMINPASSWORD':ADMIN_PASSWORD}
    
        # setup password file
        commerce_setup_helper.substitute_file_fields(response_files_path + '/otdPassword.pwd.master', response_files_path + '/otdPassword.pwd', otdPassword_replacements)
        
        # create new config
        configCommand = "\"" + TADM_COMMAND + " create-config --user=" + ADMIN_USER + " --password-file=" + response_files_path + "/otdPassword.pwd --listener-port=" + \
            VSERVER_PORT + " --server-name=" + VSERVER_NAME + " --origin-server=" + OSERVERS + " --origin-server-pool-name=" + OPOOL_NAME + " --origin-server-type=" + OSERVER_TYPE + " " + CONFIG_NAME + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, configCommand)
        
        # set load balancer algorithm
        loadDistCommand = "\"" + TADM_COMMAND + " set-origin-server-pool-prop --user=" + ADMIN_USER + " --password-file=" + response_files_path + "/otdPassword.pwd --config=" + \
            CONFIG_NAME + " --origin-server-pool=" + OPOOL_NAME + " load-distribution=" + LOAD_ALG + "\""
    
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, loadDistCommand) 

        # set health check URL
        healthCheckCommand = "\"" + TADM_COMMAND + " set-health-check-prop --user=" + ADMIN_USER + " --password-file=" + response_files_path + "/otdPassword.pwd --config=" + \
            CONFIG_NAME + " --origin-server-pool=" + OPOOL_NAME + " request-uri=" + HEALTH_CHECK_URL + " request-method=" + HEALTH_CHECK_METHOD + "\""
    
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, healthCheckCommand)                            
        
        # create new instance
        instanceCommand = "\"" + TADM_COMMAND + " create-instance --user=" + ADMIN_USER + " --password-file=" + response_files_path + "/otdPassword.pwd --config=" + CONFIG_NAME + " " + INSTANCE_HOST + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, instanceCommand)   
        
        # start the instance
        startInstanceCommand = "\"" + TADM_COMMAND + " start-instance --user=" + ADMIN_USER + " --password-file=" + response_files_path + "/otdPassword.pwd --config=" + CONFIG_NAME + " " + INSTANCE_HOST + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, startInstanceCommand)
        
        if (platform.system() == 'SunOS'):
            startStopPath = "/startStopScripts/" + service_version + "/solaris/"
        else:
            startStopPath = "/startStopScripts/" + service_version + "/"
                
        OTD_INSTANCE_NAME = 'net-' + CONFIG_NAME
        SCRIPT_NAME = 'OTD-' + CONFIG_NAME
        # copy start/stop script
        otdScript_replacements = {'OTD_PROCESS_OWNER':INSTALL_OWNER, 'OTD_INSTANCE_HOME':INSTANCE_HOME, 'OTD_INSTANCE_NAME':OTD_INSTANCE_NAME}
        commerce_setup_helper.copy_start_script(OTD_START_BOOT, full_path + startStopPath + 'OTDAdmin.master', otdScript_replacements, SCRIPT_NAME)
        
        commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "# echo " + SCRIPT_NAME + " start/stop script: /etc/init.d/" + SCRIPT_NAME + "\n\n")                        
