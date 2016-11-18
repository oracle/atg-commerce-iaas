
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

json_key = 'ATGPATCH_install'
service_name = "ATG Patch"

def install_atgpatch(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        print json_key + " config data missing from json. will not install"
        return False

    binary_path = full_path + "/binaries/atg11.1"
    response_files_path = full_path + "/responseFiles/atg11.1"
                    
    print "installing " + service_name                
    requiredFields = ['dynamoRoot', 'installOwner']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)

    INSTALL_DIR = jsonData['dynamoRoot']
    INSTALL_OWNER = jsonData['installOwner']
    PATCH_ARCHIVE = jsonData['atg_patch_archive']
    PATCH_NAME = jsonData['atg_patch_destination']
    
    path_to_patch = binary_path + "/patches/" + PATCH_ARCHIVE
    patch_destination = INSTALL_DIR + "/patch/" + PATCH_NAME
    
    if not os.path.exists(path_to_patch):
        print "patch file " + path_to_patch + " does not exist - will not install"
        return False
    
    unzipCommand = "\"" + "unzip " + path_to_patch + " -d " + INSTALL_DIR + "/patch" + "\""
    chmodCmd = "\"" + "chmod 755 " + patch_destination + "/bin/install.sh" + "\""
    installCmd = "\"" + "cd " + patch_destination + "/bin; ./install.sh < " + response_files_path + "/patches/YES.txt" + "\""    
    
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, unzipCommand)
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, chmodCmd)
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCmd)
    