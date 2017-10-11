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
import os
import ConfigParser 
import logging

logger = logging.getLogger(__name__)

installer_key = 'installer_data'
json_key = 'ATG_install'
service_name = "ATG"

def install_atg(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not install")
        return False

    if installer_key in configData:
        installerData = configData[installer_key]
    else:
        logging.error("installer json data missing. Cannot continue")
        return False    
    
    logging.info("installing " + service_name)

    config = ConfigParser.ConfigParser()
    installer_props = installerData['installer_properties']
    config_file = full_path + '/' + installer_props
    
    if (not os.path.exists(config_file)):
        logging.error("Installer config " + config_file + " not found. Halting")
        return False
    
    logging.info("config file is " + config_file)
    config.read(config_file)
    try:            
        binary_path = config.get(service_name, 'atg_binary')
    except ConfigParser.NoSectionError:
        logging.error("Config section " + service_name + " not found in config file. Halting")
        return False

    if (not os.path.exists(binary_path)):
        logging.error("Cannot find installer file " + binary_path + "   Halting")
        return
    
    response_files_path = full_path + "/responseFiles/atg11.3"  
                                        
    requiredFields = ['dynamoRoot', 'installOwner', 'installGroup', 'rmiPort', 'javaHome', 'wl_home', 'wl_domain', 'wl_adminPort', 'install_crs', 'install_csa']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    INSTALL_DIR = jsonData['dynamoRoot']
    INSTALL_OWNER = jsonData['installOwner']
    INSTALL_GROUP = jsonData['installGroup']
    RMI_PORT = jsonData['rmiPort']
    JAVA_DIR = jsonData['javaHome']
    WL_HOME = jsonData['wl_home']
    WL_DOMAIN = jsonData['wl_domain']
    WL_ADMIN_PORT = jsonData['wl_adminPort']
    INSTALL_CRS = jsonData['install_crs']
    INSTALL_CSA = jsonData['install_csa']
    INSTALL_SERVICE = jsonData['install_service']
    
    field_replacements = {'INSTALL_HOME':INSTALL_DIR, 'WEBLOGIC_HOME':WL_HOME, 'WEBLOGIC_DOMAIN':WL_DOMAIN, 'WEBLOGIC_ADMIN_PORT':WL_ADMIN_PORT, 'ATGRMI_PORT':RMI_PORT, 'JDK_PATH':JAVA_DIR}
    commerce_setup_helper.substitute_file_fields(response_files_path + '/linux/installer.properties.master', response_files_path + '/linux/installer.properties', field_replacements)
    
    # make the install tree with correct owner if needed
    commerce_setup_helper.mkdir_with_perms(INSTALL_DIR, INSTALL_OWNER, INSTALL_GROUP)
    
    installCommand = "\"" + binary_path + " -i silent -f " + response_files_path + "/linux/installer.properties" + "\"" 
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
    
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "#ATG Settings \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export DYNAMO_ROOT=" + INSTALL_DIR + "\n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export DYNAMO_HOME=$DYNAMO_ROOT/home \n\n")
    
    if (INSTALL_CRS == "true"):
        logging.info("installing CRS")

        try:            
            crs_binary_path = config.get(service_name, 'crs_binary')
        except ConfigParser.NoSectionError:
            logging.error("Config section " + service_name + " not found in config file. Halting")
            return False
    
        if (not os.path.exists(crs_binary_path)):
            logging.error("Cannot find installer file " + crs_binary_path + " - will not install")
            return   
          
        field_replacements = {'INSTALL_HOME':INSTALL_DIR}
        commerce_setup_helper.substitute_file_fields(response_files_path + '/crs/crsinstaller.properties.master', response_files_path + '/crs/crsinstaller.properties', field_replacements)
        installCommand = "\"" + crs_binary_path + " -i silent -f " + response_files_path + "/crs/crsinstaller.properties" + "\"" 
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)   
        
    if (INSTALL_CSA == "true"):
        logging.info("installing CSA")

        try:            
            csa_binary_path = config.get(service_name, 'csa_binary')
        except ConfigParser.NoSectionError:
            logging.error("Config section " + service_name + " not found in config file. Halting")
            return False
    
        if (not os.path.exists(csa_binary_path)):
            logging.error("Cannot find installer file " + csa_binary_path + " - will not install")
            return  
                  
        field_replacements = {'INSTALL_HOME':INSTALL_DIR}
        commerce_setup_helper.substitute_file_fields(response_files_path + '/csa/csainstaller.properties.master', response_files_path + '/csa/csainstaller.properties', field_replacements)
        installCommand = "\"" + csa_binary_path + " -i silent -f " + response_files_path + "/csa/csainstaller.properties" + "\"" 
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)   

    if (INSTALL_SERVICE == "true"):
        
        logging.info("installing Service")
        
        try:            
            service_binary_path = config.get(service_name, 'service_binary')
        except ConfigParser.NoSectionError:
            logging.error("Config section " + service_name + " not found in config file. Halting")
            return False
    
        if (not os.path.exists(service_binary_path)):
            logging.error("Cannot find installer file " + service_binary_path + " - will not install")
            return  
        
        field_replacements = {'INSTALL_HOME':INSTALL_DIR}
        commerce_setup_helper.substitute_file_fields(response_files_path + '/service/serviceinstaller.properties.master', response_files_path + '/service/serviceinstaller.properties', field_replacements)
        installCommand = "\"" + service_binary_path + " -i silent -f " + response_files_path + "/service/serviceinstaller.properties" + "\"" 
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)  

