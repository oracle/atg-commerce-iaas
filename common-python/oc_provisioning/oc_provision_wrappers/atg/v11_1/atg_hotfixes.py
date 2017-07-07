# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (Oracle A-Team)"
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# *************************
# ATG hotfixes - created for Natura build
# *************************

from oc_provision_wrappers import commerce_setup_helper

import os
import platform
import shutil
import logging

logger = logging.getLogger(__name__)

json_key = 'ATG_install'
service_name = "ATG"

def copy_atg_hotfixes(configData, full_path):

    if json_key in configData:
        jsonData = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not install")
        return False
        
    logging.info("copying ATG hotfixes")
    
    binary_path = full_path + "/binaries/atg11.1"
    hotfixes_path = binary_path + "/hotfixes"
    
    if not os.path.exists(hotfixes_path):
        logging.error("hotfixes dir " + hotfixes_path + " does not exist - will not install")
        return False
                         
                   
    requiredFields = ['dynamoRoot', 'installOwner', 'installGroup']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    
    INSTALL_DIR = jsonData['dynamoRoot']
    INSTALL_OWNER = jsonData['installOwner']
    INSTALL_GROUP = jsonData['installGroup']   
    
    atg_hotfix_dir = INSTALL_DIR + "/hotfixes"
    
    # make the hotfixes dir with correct owner
    commerce_setup_helper.mkdir_with_perms(atg_hotfix_dir, INSTALL_OWNER, INSTALL_GROUP)
    
    cpCmd = "\"" + "cp " + hotfixes_path + "/p20680380_111000/p20680380_111_v1_lib.jar " + atg_hotfix_dir  + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)

    cpCmd = "\"" + "cp " + hotfixes_path + "/p20663969_102/p20663969_102_v1_lib.jar " + atg_hotfix_dir  + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)         
    
    cpCmd = "\"" + "cp " + hotfixes_path + "/p18466923_111000/p18466923_111_v2_lib.jar " + atg_hotfix_dir  + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)         

    cpCmd = "\"" + "cp " + hotfixes_path + "/p17292562_111000/p17292562_111_v1_config.jar " + atg_hotfix_dir  + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)         

    cpCmd = "\"" + "cp " + hotfixes_path + "/p17292562_111000/p17292562_111_v1_lib.jar " + atg_hotfix_dir  + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)         
    
    # configs for p17292562_111000 need to be exploded into localconfig tree
    localconfig_path = INSTALL_DIR + "/home/localconfig"
    unzipCommand = "\"" + "unzip " + hotfixes_path + "/p17292562_111000/p17292562_111_v1_config.jar" + " -d " + localconfig_path + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, unzipCommand)    
    
    
    
    
    
    