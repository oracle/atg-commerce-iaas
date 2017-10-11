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
import platform
import shutil
import ConfigParser
import logging

logger = logging.getLogger(__name__)

installer_key = 'installer_data'
json_key = 'OTD_install'
service_name = "OTD"

def install_otd(configData, full_path): 
    
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
        binary_path = config.get(service_name, 'otd_binary')
    except ConfigParser.NoSectionError:
        logging.error("Config section " + service_name + " not found in config file. Halting")
        return False

    if (not os.path.exists(binary_path)):
        logging.error("Cannot find installer file " + binary_path + "   Halting")
        return    
    
    response_files_path = full_path + "/responseFiles/OTD11"
                      
    requiredFields = ['instanceHome', 'installDir', 'adminUser', 'installOwner', 'adminPassword', 'oraInventoryDir']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    
    INSTALL_OWNER = jsonData['installOwner']
    INSTANCE_HOME = jsonData['instanceHome']
    INSTALL_DIR = jsonData['installDir']
    ORACLE_INVENTORY_DIR = jsonData['oraInventoryDir']
    ORACLE_INVENTORY_GROUP = jsonData['oraInventoryGroup']
    ADMIN_USER = jsonData['adminUser']
    ADMIN_PASSWORD = jsonData['adminPassword']
    OTD_ADMIN_BOOT = jsonData['otd_startAdmin_onBoot']
    ORA_INST = "/etc/oraInst.loc"
    OTD_INSTANCE_NAME = "admin-server"

    oraInst_replacements = {'ORACLE_INVENTORY_DIR':ORACLE_INVENTORY_DIR, 'ORACLE_INVENTORY_GROUP':ORACLE_INVENTORY_GROUP}
    otdPassword_replacements = {'TADM_ADMINPASSWORD':ADMIN_PASSWORD}          

    # if oraInst.loc doesn't already exist, we need to make one
    if not os.path.isfile(ORA_INST):
        commerce_setup_helper.substitute_file_fields(response_files_path + '/oraInst.loc.master', response_files_path + '/oraInst.loc', oraInst_replacements)
        shutil.copyfile(response_files_path + "/oraInst.loc" , ORA_INST)
        commerce_setup_helper.change_file_owner(ORA_INST, INSTALL_OWNER, ORACLE_INVENTORY_GROUP)
        os.chmod(ORA_INST, 0664) 
    
    # make the install tree with correct owner if needed
    commerce_setup_helper.mkdir_with_perms(INSTALL_DIR, INSTALL_OWNER, ORACLE_INVENTORY_GROUP)
    
    # exec the install command
    installCommand = "\"" + binary_path + " -silent -waitforcompletion -invPtrLoc /etc/oraInst.loc ORACLE_HOME=" + INSTALL_DIR + " SKIP_SOFTWARE_UPDATES=true\"" 
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)

    # setup password file
    commerce_setup_helper.substitute_file_fields(response_files_path + '/otdPassword.pwd.master', response_files_path + '/otdPassword.pwd', otdPassword_replacements)

    # install patches if any were listed
    patch_otd(configData, full_path) 
    
    # exec base admin server creation
    configCommand = "\"" + INSTALL_DIR + "/bin/tadm configure-server --user=" + ADMIN_USER + " --instance-home=" + INSTANCE_HOME + " --password-file=" + response_files_path + "/otdPassword.pwd\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, configCommand)
    
    if (platform.system() == 'SunOS'):
        startStopPath = "/startStopScripts/solaris/bootScripts/"
    else:
        startStopPath = "/startStopScripts/bootScripts/"
            
    # copy start/stop script
    otdScript_replacements = {'OTD_PROCESS_OWNER':INSTALL_OWNER, 'OTD_INSTANCE_HOME':INSTANCE_HOME, 'OTD_INSTANCE_NAME':OTD_INSTANCE_NAME}
    commerce_setup_helper.copy_start_script(OTD_ADMIN_BOOT, full_path + startStopPath + 'OTDAdmin.master', otdScript_replacements)

    # fire up the otd admin server    
    startCmd = "/etc/init.d/OTDAdmin"
    commerce_setup_helper.exec_cmd(startCmd + " start")

    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "# echo " + service_name + " start/stop script: " + startCmd + "\n\n")    
  
def patch_otd(configData, full_path):
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not patch")
        return

    if installer_key in configData:
        installerData = configData[installer_key]
    else:
        logging.error("installer json data missing. Cannot continue")
        return False        
            
    config = ConfigParser.ConfigParser()
    installer_props = installerData['installer_properties']
    config_file = full_path + '/' + installer_props
    
    if (not os.path.exists(config_file)):
        logging.error("Installer config " + config_file + " not found. Halting")
        return False
    
    logging.info("config file is " + config_file)
    
    config.read(config_file)
    try:            
        patches_path = config.get(service_name, 'otd_patches')
    except ConfigParser.NoSectionError:
        logging.error("Config section " + service_name + " not found in config file. Halting")
        return False

    if (not os.path.exists(patches_path)):
        logging.error("Cannot find installer file " + patches_path + "   Halting")
        return    
        
    # json key containing patch files
    patchKey = "otd_patches";
                                   
    requiredFields = ['installDir', 'installOwner']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    INSTALL_DIR = jsonData['installDir']
    INSTALL_OWNER = jsonData['installOwner']
    PATCH_FILES = None
    
    # if the patches key was provided, get the list of patches to apply
    if patchKey in jsonData:
        PATCH_FILES = jsonData['otd_patches']
        
    
    if PATCH_FILES:
        logging.info("patching " + service_name) 
        patches = PATCH_FILES.split(',')
        patchList = []
        patchScript = INSTALL_DIR + "/OPatch/opatch"
        tmpPatchDir = "/tmp/otdpatches"
        for patch in patches:
            # get list of patches - comma separated
            patchParts = patch.split('_')
            # get just the patch numbner
            patchNum = patchParts[0][1:]
            # keep a running list of all patch numbers
            patchList.append(patchNum)
            if not os.path.exists(patches_path + "/" + patch):
                logging.error("patch file " + patches_path + "/" + patch + " missing - will not install")
                return
            # unzip patch to /tmp. This will create a dir with the patchNum as the name
            unzipCommand = "\"" + "unzip " + patches_path + "/" + patch + " -d " + tmpPatchDir + "\""
            commerce_setup_helper.exec_as_user(INSTALL_OWNER, unzipCommand)
        patchCommand = "\"" + patchScript + " napply " + tmpPatchDir + " -silent -id " + ','.join(patchList) + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, patchCommand)
        # cleanup our files from /tmp
        shutil.rmtree(tmpPatchDir, ignore_errors=True)    
