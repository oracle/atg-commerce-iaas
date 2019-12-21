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
import logging

logger = logging.getLogger(__name__)

json_key = 'WEBLOGIC_common'
service_name = "WebLogic"

def install_weblogic(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not install")
        return
    
    logging.info("installing " + service_name)
    
    binary_path = full_path + "/binaries/wls-12.2.1"
    response_files_path = full_path + "/responseFiles/wls-12.2.1"
    #install_exec = "fmw_12.2.1.2.0_wls.jar"
    install_exec = "fmw_12.2.1.3.0_wls.jar"
    full_exec_path = binary_path + "/" + install_exec
    
    if not os.path.exists(full_exec_path):
        logging.error("Binary " + full_exec_path + " does not exist - will not install")
        return False    
                    
                    
    requiredFields = ['middlewareHome', 'installOwner', 'installGroup', 'oraInventoryDir']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    INSTALL_DIR = jsonData['middlewareHome']
    INSTALL_OWNER = jsonData['installOwner']
    INSTALL_GROUP = jsonData['installGroup']
    ORACLE_INVENTORY_DIR = jsonData['oraInventoryDir']
    ORA_INST = "/etc/oraInst.loc"
    
    oraInst_replacements = {'ORACLE_INVENTORY_DIR':ORACLE_INVENTORY_DIR, 'ORACLE_INVENTORY_GROUP':INSTALL_GROUP}
    
    # if oraInst.loc doesn't already exist, we need to make one
    if not os.path.isfile(ORA_INST):
        commerce_setup_helper.substitute_file_fields(response_files_path + '/oraInst.loc.master', response_files_path + '/oraInst.loc', oraInst_replacements)
        shutil.copyfile(response_files_path + "/oraInst.loc" , ORA_INST)
        commerce_setup_helper.change_file_owner(ORA_INST, INSTALL_OWNER, INSTALL_GROUP)
        os.chmod(ORA_INST, 0664) 
        
    wl_replacements = {'INSTALL_DIR':INSTALL_DIR}
    commerce_setup_helper.substitute_file_fields(response_files_path + '/install.rsp.master', response_files_path + '/install.rsp', wl_replacements)
    
    # make the install tree with correct owner if needed
    commerce_setup_helper.mkdir_with_perms(INSTALL_DIR, INSTALL_OWNER, INSTALL_GROUP)
        
    # install wl
    if (platform.system() == 'SunOS'):
        installCommand = "\"" + "java -d64 -jar "
    else:
        installCommand = "\"" + "java -jar "    
    installCommand = installCommand + full_exec_path + " -silent -invPtrLoc " + ORA_INST + " -responseFile " + response_files_path + "/install.rsp" + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
    
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "#WebLogic Settings \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export MW_HOME=" + INSTALL_DIR + "\n\n")

    JAVA_RAND = ""
    # if linux/Solaris, change random, This is faster in some implementations.
    if (platform.system() == "SunOS"):
        JAVA_RAND = "-Djava.security.egd=file:///dev/urandom"
    else:
        JAVA_RAND = "-Djava.security.egd=file:/dev/./urandom"
            
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, 'export CONFIG_JVM_ARGS=\"' + JAVA_RAND + ' \" \n')
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, 'export JAVA_OPTIONS=\"' + JAVA_RAND + ' \" \n')

    #add variable for the opatch utility
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export OPATCH_NO_FUSER=TRUE \n")

#as a workaround to a bug install patches after domain gets created
    # apply Opatch before applying the WLS PSU
    #opatch_weblogic(configData, full_path)
    
    # install patches if any were listed
    #patch_weblogic(configData, full_path)    

def opatch_weblogic(configData, full_path):
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        logging.error(json_key + " config data for opatch missing from json. will not install")
        return

    logging.info("patching the OPatch... " )
    binary_path = full_path + "/binaries/wls-12.2.1"
    patches_path = binary_path + "/patches"

    requiredFields = ['middlewareHome', 'installOwner', 'installGroup']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    INSTALL_DIR = jsonData['middlewareHome']
    INSTALL_OWNER = jsonData['installOwner']
    OPATCH_FILE = "p28186730_139400_Generic.zip"
    
    # if the opatch key was provided, get the opatch to apply
    if not os.path.exists(patches_path + "/" + OPATCH_FILE):
        logging.error("opatch file " + patches_path + "/" + OPATCH_FILE + " missing - will not install")
        return


    patchScript = INSTALL_DIR + "/OPatch/opatch"
    unzipCommand = "\"" + "unzip " + patches_path + "/" + OPATCH_FILE + " -d " + patches_path + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, unzipCommand)

    installCommand = "\"" + "java -jar "
    installCommand = installCommand + patches_path + "/" + "6880880" + "/" + "opatch_generic.jar" + " -silent " + "oracle_home=" + INSTALL_DIR + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
    
def patch_weblogic(configData, full_path):
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not install")
        return

    logging.info("patching the PSU Patches... " )
    binary_path = full_path + "/binaries/wls-12.2.1"
    patches_path = binary_path + "/patches"
    # json key containing patch files
    patchKey = "wl_patches"
                                   
    requiredFields = ['middlewareHome', 'installOwner', 'installGroup']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    INSTALL_DIR = jsonData['middlewareHome']
    INSTALL_OWNER = jsonData['installOwner']
    PATCH_FILES = None
    
    # if the patches key was provided, get the list of patches to apply
    if patchKey in jsonData:
        PATCH_FILES = jsonData['wl_patches']
    
    if PATCH_FILES:
        logging.info("patching " + service_name) 
        patches = PATCH_FILES.split(',')
        patchList = []
        patchScript = INSTALL_DIR + "/OPatch/opatch"
        tmpPatchDir = "/tmp/wlpatches"
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
        patchCommand = "\"" + patchScript + " napply " + tmpPatchDir + " -jre /usr/java/latest" + " -silent -id " + ','.join(patchList) + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, patchCommand)
        # cleanup our files from /tmp
        shutil.rmtree(tmpPatchDir)
