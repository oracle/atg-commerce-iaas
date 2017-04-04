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
import time
import logging

logger = logging.getLogger(__name__)

json_key = 'ORACLE_11g_clone'
service_name = "Oracle DB clone"

def clone_oracle(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not install")
        return
    logging.info("installing " + service_name)

    INSTALL_OWNER = jsonData['installOwner']
    ORACLE_HOME = jsonData['oracleHome']
    ORIG_HOST = jsonData['originalHost']
    NEW_HOST = jsonData['newHost']
    ORACLE_SID = jsonData['oracleSID']
    UPDATE_DB_CONSOLE = jsonData['updateDBConsole']     
            
    db_script = "/etc/init.d/oracleDatabase"
    db_console_script = "/etc/init.d/oracleDBconsole"
    stop_db_cmd = db_script + " stop"
    stop_db_console_cmd = db_console_script + " stop"
    start_db_cmd = db_script + " start"
    start_db_console_cmd = db_console_script + " start"
 
        
    tns_path = ORACLE_HOME + "/network/admin/tnsnames.ora"
    lsnr_path = ORACLE_HOME + "/network/admin/listener.ora"   
    
    if not os.path.exists(tns_path):
        logging.error("tnsnames.ora not found at " + tns_path + " - will not proceed")
        return False

    # stop db
    commerce_setup_helper.exec_cmd(stop_db_cmd)
    
    # stop console
    commerce_setup_helper.exec_cmd(stop_db_console_cmd)
            
    tns_replacements = {}
    lsnr_replacements = {}    
        
    if (ORIG_HOST and NEW_HOST):
        tns_replacements[ORIG_HOST] = NEW_HOST
        lsnr_replacements[ORIG_HOST] = NEW_HOST       
    
    # update tnsnames
    if tns_replacements:
        if not os.path.exists(tns_path):
            logging.warn("tnsnames.ora not found at " + tns_path + " - cannot modify")
        else:
            # backup tnsnames
            timestr = time.strftime("%Y%m%d-%H%M%S")
            installCommand = "\"" + "cp " + tns_path + " " + tns_path + "." + timestr + "\""
            commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
            commerce_setup_helper.substitute_file_fields(tns_path, tns_path, tns_replacements)

    # update listener
    if lsnr_replacements:
        if not os.path.exists(lsnr_path):
            logging.warn("listener.ora not found at " + lsnr_path + " - cannot modify")
        else:      
            # backup listener
            timestr = time.strftime("%Y%m%d-%H%M%S")
            installCommand = "\"" + "cp " + lsnr_path + " " + lsnr_path + "." + timestr + "\""
            commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
            commerce_setup_helper.substitute_file_fields(lsnr_path, lsnr_path, tns_replacements)
        
    # update db name
    orig_db_name = ORACLE_HOME + "/" + ORIG_HOST + "_" + ORACLE_SID
    new_db_name = ORACLE_HOME + "/" + NEW_HOST + "_" + ORACLE_SID
    if not os.path.exists(orig_db_name):
        logging.error("db path not found at " + orig_db_name + " - cannot modify")
    else:
        mv_cmd = "\"" + "mv " + orig_db_name + " " + new_db_name + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, mv_cmd)

    # update db console
    if (UPDATE_DB_CONSOLE == "true") :
        PORT = jsonData['lsnrPort']
        ORACLE_PW = jsonData['adminPW']
        orig_db_console = ORACLE_HOME + "/oc4j/j2ee/OC4J_DBConsole_" + ORIG_HOST + "_" + ORACLE_SID
        new_db_console = ORACLE_HOME + "/oc4j/j2ee/OC4J_DBConsole_" + NEW_HOST + "_" + ORACLE_SID
        if not os.path.exists(orig_db_console):
            logging.warn("db console not found at " + orig_db_console + " - cannot modify")
        else:
            mv_cmd = "\"" + "mv " + orig_db_console + " " + new_db_console + "\""
            commerce_setup_helper.exec_as_user(INSTALL_OWNER, mv_cmd)
            
            # db must be running for emca to exec. make sure
            # start db
            commerce_setup_helper.exec_cmd(start_db_cmd)    
            
            emca_params = "-SID " + ORACLE_SID + " -PORT " + PORT + " -SYS_PWD " + ORACLE_PW + " -SYSMAN_PWD " +  ORACLE_PW + " -DBSNMP_PWD " + ORACLE_PW
            drop_repo_cmd =   "\"" + ORACLE_HOME + "/bin/emca -deconfig dbcontrol db -repos drop -silent " + emca_params + "\""
            create_repo_cmd =   "\"" + ORACLE_HOME + "/bin/emca -config dbcontrol db -repos create -silent " + emca_params + "\""
            commerce_setup_helper.exec_as_user(INSTALL_OWNER, drop_repo_cmd)
            commerce_setup_helper.exec_as_user(INSTALL_OWNER, create_repo_cmd)
        
    # stop db
    commerce_setup_helper.exec_cmd(stop_db_cmd)
    
    # stop console
    commerce_setup_helper.exec_cmd(stop_db_console_cmd)
    
    # start db
    commerce_setup_helper.exec_cmd(start_db_cmd)
    
    if (UPDATE_DB_CONSOLE == "true") :
        # start dbconsole
        commerce_setup_helper.exec_cmd(start_db_console_cmd)       
