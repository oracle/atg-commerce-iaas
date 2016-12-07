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

from oc_provision_wrappers import commerce_setup_helper


json_key = 'advanced_storage'

def advanced_storage(configData, full_path): 
    
    if json_key in configData:
        jsonArray = configData[json_key]
    else:
        print json_key + " config data missing from json. will not install"
        return                
    
    for jsonData in jsonArray:
        
        requiredFields = ['device', 'mountPoint', 'mountOwner', 'mountGroup']
        commerce_setup_helper.check_required_fields(jsonData, requiredFields)
        DEVICE = jsonData['device']
        MOUNT_POINT = jsonData['mountPoint']
        MOUNT_OWNER = jsonData['mountOwner']
        MOUNT_GROUP = jsonData['mountGroup']
        
        FSTAB_ENTRY = DEVICE + "  " + MOUNT_POINT + "  ext4  defaults  0 0 \n"
        
        print "creating and mounting storage on device " + DEVICE + " at " + MOUNT_POINT + " \n"
        
        createCmd = "mkfs -t ext4 " + DEVICE 
        mountCmd = "mount " + DEVICE + " " + MOUNT_POINT + " -t ext4"
        mountOwnerCmd = "chown " + MOUNT_OWNER + ":" + MOUNT_GROUP + " " + MOUNT_POINT
        
        if not (os.path.exists(MOUNT_POINT)):
            os.mkdir(MOUNT_POINT, 0755)            
        
        commerce_setup_helper.exec_cmd(createCmd)
        commerce_setup_helper.exec_cmd(mountCmd)
        commerce_setup_helper.exec_cmd(mountOwnerCmd)
    
        with open("/etc/fstab", "a") as myfile:
            myfile.write(FSTAB_ENTRY)
        myfile.close()    
      
    
    
                
