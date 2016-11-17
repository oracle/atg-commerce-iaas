
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

json_key = 'ATGPATCH_install'

def post_install_cmds(configData, full_path): 
    
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        print json_key + " config data missing from json. will not install"
        return

    print "executing post patch install tasks"
    
    INSTALL_DIR = jsonData['dynamoRoot']
    INSTALL_OWNER = jsonData['installOwner']
    
    # fix manifest                
    patch_manifest(INSTALL_DIR, INSTALL_OWNER)
                        
    # fix crs after patch
    patch_crs(configData, full_path)
    
def patch_manifest(INSTALL_DIR, INSTALL_OWNER):
    # fix missing manifest entry that cause jps-config.xml to not get pulled into standalone ears
    MANIFEST_TO_UPDATE = INSTALL_DIR + "/home/META-INF/MANIFEST.MF"
    fixJPScmd = "\"" + "echo >> " + MANIFEST_TO_UPDATE + \
                "; echo 'Name: security' >> " + MANIFEST_TO_UPDATE + \
                "; echo 'ATG-Assembler-Import-File: true' >> " + MANIFEST_TO_UPDATE + "\""
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, fixJPScmd)    
    
def patch_crs(configData, full_path):
    """
    patch1 has a bug where it does not update CRS with new taglibs. Patch it here.
    """   
    atginstall_json_key = 'ATG_install'
    if atginstall_json_key not in configData:
        return
    
    jsonData = configData[atginstall_json_key]
    INSTALL_DIR = jsonData['dynamoRoot']
    INSTALL_OWNER = jsonData['installOwner']
    INSTALL_CRS = jsonData['install_crs']
    
    if INSTALL_CRS:     
        # If patch1 is installed, these are not updated. fix it.
        cpCmd = "\"" + "cp " + INSTALL_DIR + "/DAS/taglib/dspjspTaglib/1.0/lib/dspjspTaglib1_0.jar " + INSTALL_DIR + "/CommerceReferenceStore/Store/Storefront/j2ee-apps/Storefront/store.war/WEB-INF/lib" + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)
        cpCmd = "\"" + "cp " + INSTALL_DIR + "/DAS/taglib/dspjspTaglib/1.0/lib/dspjspTaglib1_0.jar " + INSTALL_DIR + "/CommerceReferenceStore/Store/Storefront/j2ee-apps/Storefront/storedocroot.war/WEB-INF/lib" + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)
        cpCmd = "\"" + "cp " + INSTALL_DIR + "/DAS/taglib/dspjspTaglib/1.0/lib/dspjspTaglib1_0.jar " + INSTALL_DIR + "/CommerceReferenceStore/Store/Fluoroscope/j2ee-apps/Fluoroscope/fluoroscope.war/WEB-INF/lib" + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)
        cpCmd = "\"" + "cp " + INSTALL_DIR + "/DAS/taglib/dspjspTaglib/1.0/lib/dspjspTaglib1_0.jar " + INSTALL_DIR + "/CommerceReferenceStore/Store/DCS-CSR/j2ee-apps/DCS-CSR/CSRHelper.war/WEB-INF/lib" + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)
        cpCmd = "\"" + "cp " + INSTALL_DIR + "/DAS/taglib/dspjspTaglib/1.0/lib/dspjspTaglib1_0.jar " + INSTALL_DIR + "/CommerceReferenceStore/Store/EStore/Versioned/j2ee-apps/Versioned/store-merchandising.war/WEB-INF/lib" + "\""
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, cpCmd)         
    
    
    
