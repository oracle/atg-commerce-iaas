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

from oc_provision_wrappers import commerce_setup_helper


json_key = 'OTD_install'
service_name = "OTD"

def install_otd(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        print json_key + " config data missing from json. will not install"
        return False

    print "installing " + service_name 
    
    if (platform.system() == "SunOS"):
        binary_path = full_path + "/binaries/OTD11.1.1.9/solaris"
    else:
        binary_path = full_path + "/binaries/OTD11.1.1.9"
        
    install_exec = "/Disk1/runInstaller"
    
    response_files_path = full_path + "/responseFiles/OTD11"
    
    full_exec_path = binary_path + install_exec
    
    if not os.path.exists(full_exec_path):
        print "Binary " + full_exec_path + " does not exist - will not install"
        return False  
                      
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
    installCommand = "\"" + binary_path + "/Disk1/runInstaller -silent -waitforcompletion -invPtrLoc /etc/oraInst.loc ORACLE_HOME=" + INSTALL_DIR + " SKIP_SOFTWARE_UPDATES=true\"" 
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)

    # setup password file
    commerce_setup_helper.substitute_file_fields(response_files_path + '/otdPassword.pwd.master', response_files_path + '/otdPassword.pwd', otdPassword_replacements)
    
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
  
    
