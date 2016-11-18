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
import os

json_key = 'ENDECA_install'
service_name = "PlatformServices"
endeca_version = "11.2.0"

def install_platformServices(configData, full_path): 
        
    endecaData = configData[json_key]
    requiredFields = ['installOwner', 'installGroup']
    commerce_setup_helper.check_required_fields(endecaData, requiredFields)
    INSTALL_OWNER = endecaData['installOwner']
    INSTALL_GROUP = endecaData['installGroup']
    if 'platformServices' in endecaData:
        jsonData = endecaData['platformServices']
        requiredFields = ['endecaRoot', 'eacPort', 'eacShutdownPort', 'mdexRoot']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    else:
        print service_name + " config data missing from json. will not install"
        return
    
    print "installing " + service_name
    
    if (platform.system() == "SunOS"):
        binary_path = full_path + "/binaries/endeca11.2/solaris"
        install_exec = "/Platform_Install/OCplatformservices11.2.0-Solaris.bin"
    else:
        binary_path = full_path + "/binaries/endeca11.2"
        install_exec = "/Platform_Install/OCplatformservices11.2.0-Linux64.bin"
        
    response_files_path = full_path + "/responseFiles/endeca11.2"
    
    full_exec_path = binary_path + install_exec
    
    if not os.path.exists(full_exec_path):
        print "Binary " + full_exec_path + " does not exist - will not install"
        return False        
        
    if jsonData is not None:
        ENDECA_ROOT = jsonData['endecaRoot']
        MDEX_ROOT = jsonData['mdexRoot']
        EAC_PORT = jsonData['eacPort']
        EAC_SHUTDOWN_PORT = jsonData['eacShutdownPort']
        START_ON_BOOT = jsonData['start_onBoot']
        # make the install tree with correct owner if needed
        commerce_setup_helper.mkdir_with_perms(ENDECA_ROOT, INSTALL_OWNER, INSTALL_GROUP)

        # data field to replace in our silent installer file
        field_replacements = {'INSTALLATION_DIR':ENDECA_ROOT, 'MDEX_INST_ROOT':MDEX_ROOT, 'EAC_PORT':EAC_PORT, 'EAC_SHUTDOWN_PORT':EAC_SHUTDOWN_PORT} 

        commerce_setup_helper.substitute_file_fields(response_files_path + '/platform_response.rsp.master', response_files_path + '/platform_response.rsp', field_replacements)
        
        installCommand = "\"" + full_exec_path + " -i silent -f " + response_files_path + '/platform_response.rsp' + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
         
        # add bashrc entries
        commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "source " + ENDECA_ROOT + "/endeca/PlatformServices/workspace/setup/installer_sh.ini \n")
        
        # copy start/stop script
        ENDECA_HOME = ENDECA_ROOT + "/endeca"
        MDEX_SETUP = MDEX_ROOT + "/mdex_setup_sh.ini"
        PLATFORM_SETUP = ENDECA_HOME + "/PlatformServices/workspace/setup/installer_sh.ini"
        script_replacements = {'ENDECA_PROCESS_OWNER':INSTALL_OWNER, 'ENDECA_INSTALL_ROOT':ENDECA_HOME, "MDEX_SETUP":MDEX_SETUP, "PLATFORM_SETUP":PLATFORM_SETUP, "INSTALL_VERSION":endeca_version}
        commerce_setup_helper.copy_start_script(START_ON_BOOT, full_path + '/startStopScripts/bootScripts/platformServices.master', script_replacements)
        
        # fire up the server    
        startCmd = "/etc/init.d/platformServices"
        commerce_setup_helper.exec_cmd(startCmd + " start")
        
        commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "# echo Endeca " + service_name + " start/stop script: " + startCmd + "\n")
