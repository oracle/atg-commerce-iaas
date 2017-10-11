
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

installer_key = 'installer_data'
json_key = 'ATGPATCH_install'
service_name = "ATG_Patch"

logger = logging.getLogger(__name__)

def install_atgpatch(configData, full_path): 
    
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
    
    response_files_path = full_path + "/responseFiles/atg11.2"
                    
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
        patches_path = config.get(service_name, 'atg_patches')
    except ConfigParser.NoSectionError:
        logging.error("Config section " + service_name + " not found in config file. Halting")
        return False

    if (not os.path.exists(patches_path)):
        logging.error("Cannot find installer file " + patches_path + "   Halting")
        return
                        
    requiredFields = ['dynamoRoot', 'installOwner']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    INSTALL_DIR = jsonData['dynamoRoot']
    INSTALL_OWNER = jsonData['installOwner']
    PATCH_ARCHIVE = jsonData['atg_patch_archive']
    PATCH_NAME = jsonData['atg_patch_destination']
    
    path_to_patch = patches_path + "/" + PATCH_ARCHIVE
    patch_destination = INSTALL_DIR + "/patch/" + PATCH_NAME
    
    if not os.path.exists(path_to_patch):
        logging.error("patch file " + path_to_patch + " does not exist - will not install")
        return False
    
    unzipCommand = "\"" + "unzip " + path_to_patch + " -d " + INSTALL_DIR + "/patch" + "\""
    chmodCmd = "\"" + "chmod 755 " + patch_destination + "/bin/install.sh" + "\""
    installCmd = "\"" + "cd " + patch_destination + "/bin; ./install.sh < " + response_files_path + "/patches/YES.txt" + "\""    
    
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, unzipCommand)
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, chmodCmd)
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCmd)
    