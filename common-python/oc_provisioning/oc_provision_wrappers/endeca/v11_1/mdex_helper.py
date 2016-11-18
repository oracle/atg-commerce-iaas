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
service_name = "MDEX"

def install_mdex(configData, full_path): 
    endecaData = configData[json_key]
    requiredFields = ['installOwner', 'installGroup']
    commerce_setup_helper.check_required_fields(endecaData, requiredFields)
    INSTALL_OWNER = endecaData['installOwner']
    INSTALL_GROUP = endecaData['installGroup']
    if 'mdex' in endecaData:
        jsonData = endecaData['mdex']
        requiredFields = ['endecaRoot']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    else:
        print service_name + " config data missing from json. will not install"
        return
    
    print "installing " + service_name
    
    if (platform.system() == "SunOS"):
        binary_path = full_path + "/binaries/endeca11.1/solaris"
        install_exec = "/MDEX_Install/OCmdex6.5.1-Solaris_829811.sh"
    else:
        binary_path = full_path + "/binaries/endeca11.1"
        install_exec = "/MDEX_Install/OCmdex6.5.1-Linux64_829811.sh"
        
    full_exec_path = binary_path + install_exec
    
    if not os.path.exists(full_exec_path):
        print "Binary " + full_exec_path + " does not exist - will not install"
        return False      
        
    if jsonData is not None:
        
        ENDECA_ROOT = jsonData['endecaRoot']
        # make the install tree with correct owner if needed
        commerce_setup_helper.mkdir_with_perms(ENDECA_ROOT, INSTALL_OWNER, INSTALL_GROUP)

        installCommand = "\"" + full_exec_path + " --target " + ENDECA_ROOT + "\""
        # print "command is " + installCommand
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
         
        # add bashrc entries
        commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
        commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "#Endeca Settings \n")
        commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
        commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "source " + ENDECA_ROOT + "/endeca/MDEX/6.5.1/mdex_setup_sh.ini \n")
        commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export ENDECA_HOME=" + ENDECA_ROOT + "/endeca \n")        
