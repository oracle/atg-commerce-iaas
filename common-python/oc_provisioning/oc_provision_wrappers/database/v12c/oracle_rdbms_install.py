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

import fileinput
import platform
import os

from oc_provision_wrappers import commerce_setup_helper


json_key = 'ORACLE_RDBMS_install'
service_name = "Oracle DB"

def install_oracle(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        print json_key + " config data missing from json. will not install"
        return
    
    print "installing " + service_name
    
    if (platform.system() == "SunOS"):
        binary_path = full_path + "/binaries/oracleDB12c/solaris"
    else:
        binary_path = full_path + "/binaries/oracleDB12c"
        
    response_files_path = full_path + "/responseFiles/oracle12c"

    install_exec = "/database/runInstaller"
    full_exec_path = binary_path + install_exec
    
    if not os.path.exists(full_exec_path):
        print "Binary " + full_exec_path + " does not exist - will not install"
        return False
                        
                    
    requiredFields = ['oracleBase', 'installOwner', 'installGroup', 'installHost', 'oraInventoryDir', 'oracleHome', 'oracleSID', 'pdbName', 'adminPW', 'dbStorageLoc']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    ORACLE_BASE = jsonData['oracleBase']
    INSTALL_OWNER = jsonData['installOwner']
    INSTALL_GROUP = jsonData['installGroup']
    INSTALL_HOST = jsonData['installHost']
    ORACLE_INVENTORY_DIR = jsonData['oraInventoryDir']
    ORACLE_HOME = jsonData['oracleHome']
    ORACLE_SID = jsonData['oracleSID']
    PDB_NAME = jsonData['pdbName']
    ORACLE_PW = jsonData['adminPW']
    DB_FILE_DIR = jsonData['dbStorageLoc']
    ORACLE_BOOT = jsonData['db_onBoot']
        
    oracle_replacements = {'BASE_DIR':ORACLE_BASE, 'IGROUP':INSTALL_GROUP, 'INSTALL_HOST':INSTALL_HOST, 'INVENTORY_DIR':ORACLE_INVENTORY_DIR, 'PRODUCT_HOME':ORACLE_HOME,
                            'GLOBAL_DBNAME':ORACLE_SID, 'PDB_NAME':PDB_NAME, 'ORA_PW':ORACLE_PW, 'DB_FILE_DIR':DB_FILE_DIR, }
            
    commerce_setup_helper.substitute_file_fields(response_files_path + '/db.rsp.master', response_files_path + '/db.rsp', oracle_replacements)
    commerce_setup_helper.substitute_file_fields(response_files_path + '/dbca.rsp.master', response_files_path + '/dbca.rsp', oracle_replacements)
    
    # make the install trees with correct owner if needed
    commerce_setup_helper.mkdir_with_perms(ORACLE_BASE, INSTALL_OWNER, INSTALL_GROUP)
    commerce_setup_helper.mkdir_with_perms(ORACLE_INVENTORY_DIR, INSTALL_OWNER, INSTALL_GROUP)
    commerce_setup_helper.mkdir_with_perms(ORACLE_HOME, INSTALL_OWNER, INSTALL_GROUP)
    commerce_setup_helper.mkdir_with_perms(DB_FILE_DIR, INSTALL_OWNER, INSTALL_GROUP)
    
    # install db
    installCommand = "\"" + full_exec_path + " -silent -waitforcompletion -responseFile " + response_files_path + "/db.rsp" + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
    
    invCmd = ORACLE_INVENTORY_DIR + "/orainstRoot.sh"
    commerce_setup_helper.exec_cmd(invCmd)

    rootCmd = ORACLE_HOME + "/root.sh"
    commerce_setup_helper.exec_cmd(rootCmd)    
    
    postInstallCmd = "\"" + ORACLE_HOME + "/cfgtoollogs/configToolAllCommands RESPONSE_FILE=" + response_files_path + "/db.rsp" + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, postInstallCmd)
    
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "#Oracle Settings \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export ORACLE_HOME=" + ORACLE_HOME + "\n")  
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export ORACLE_SID=" + ORACLE_SID + "\n")    
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export PATH=$PATH:" + ORACLE_HOME + "/bin \n") 
    
    # copy start/stop script
    script_replacements = {'ORACLE_HOME':ORACLE_HOME, 'ORACLE_PROCESS_OWNER':INSTALL_OWNER}
    commerce_setup_helper.copy_start_script(ORACLE_BOOT, full_path + '/startStopScripts/bootScripts/oracleDatabase.master', script_replacements)
    # commerce_setup_helper.copy_start_script(ORACLE_BOOT, full_path + '/startStopScripts/bootScripts/oracleDBconsole.master', script_replacements)
    
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "# echo " + service_name + " start/stop script: /etc/init.d/oracleDatabase \n")
    # not used for 12c install - using em express instead
    # commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "# echo database console start/stop script: /etc/init.d/oracleDBconsole \n\n")
    
    install_listener(INSTALL_OWNER, ORACLE_HOME, response_files_path)
    
    install_sampledb(INSTALL_OWNER, ORACLE_HOME, response_files_path)
    
    if (platform.system() == "SunOS"):
        oratab_file = "/var/opt/oracle/oratab"
    else:
        oratab_file = "/etc/oratab"
        
    # set our DB to autostart in the future
    line_to_replace = ORACLE_SID + ":" + ORACLE_HOME + ":" "N"
    replace_with = ORACLE_SID + ":" + ORACLE_HOME + ":" "Y"
    
    for line in fileinput.input(oratab_file, inplace=True): 
        print line.rstrip().replace(line_to_replace, replace_with)   
    
    

def install_listener(INSTALL_OWNER, ORACLE_HOME, response_files_path):
    postInstallCmd = "\"" + ORACLE_HOME + "/bin/netca -silent -responseFile " + response_files_path + "/netca.rsp" + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, postInstallCmd)      
    
def install_sampledb(INSTALL_OWNER, ORACLE_HOME, response_files_path):
    postInstallCmd = "\"" + ORACLE_HOME + "/bin/dbca -silent -responseFile " + response_files_path + "/dbca.rsp" + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, postInstallCmd)          
  
