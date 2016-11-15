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
from oc_provision_wrappers import commerce_setup_helper

json_key = 'JAVA_install'
service_name = "Java"

def install_java(configData, full_path): 
        
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        print service_name + " config data missing from json. will not install"
        return

    if (platform.system() == "SunOS"):
        binary_path = full_path + "/binaries/java1.8/solaris"
    else:
        binary_path = full_path + "/binaries/java1.8"
                
    requiredFields = ['javaHome', 'installOwner', 'installGroup']
    commerce_setup_helper.check_required_fields(jsonData, requiredFields)
    INSTALL_OWNER = jsonData['installOwner']
    INSTALL_GROUP = jsonData['installGroup']
    JAVA_HOME = jsonData['javaHome']

    commerce_setup_helper.mkdir_with_perms(JAVA_HOME, INSTALL_OWNER, INSTALL_GROUP)
    
    # solaris setup is different
    if (platform.system() == "SunOS"):
        install64bitCommand = "\"" + "cd " + JAVA_HOME + "; tar zxf " + binary_path + "/jdk-8u73-solaris-sparcv9.tar.gz " + "\""
    else:
        installCommand = "\"" + "tar zxf " + binary_path + "/jdk-8u73-linux-x64.tar.gz -C " + JAVA_HOME + "\""
        
    linkCommand = "\"" + "ln -sf " + JAVA_HOME + "/jdk1.8.0_73 " + JAVA_HOME + "/latest" + "\""    
    
    if (platform.system() == "SunOS"):
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, install64bitCommand)
    else:
        commerce_setup_helper.exec_as_user(INSTALL_OWNER, installCommand)
        
    if (os.path.exists(JAVA_HOME + "/latest") or  os.path.islink(JAVA_HOME + "/latest")):
        os.remove(JAVA_HOME + "/latest")
    os.symlink(JAVA_HOME + "/jdk1.8.0_73", JAVA_HOME + "/latest")
               
    # commerce_setup_helper.exec_as_user(INSTALL_OWNER, linkCommand)
    if (platform.system() != "SunOS"):
        if (os.path.exists('/usr/bin/java') or  os.path.islink('/usr/bin/java')):
            os.remove('/usr/bin/java')
        os.symlink(JAVA_HOME + '/latest/bin/java', '/usr/bin/java')

    # add bashrc entries
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "#Java Settings \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "##################### \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export JAVA_HOME=" + JAVA_HOME + "/latest \n")
    commerce_setup_helper.add_to_bashrc(INSTALL_OWNER, "export PATH=" + JAVA_HOME + "/latest/bin:$PATH \n\n")
    
    os.environ['JAVA_HOME'] = JAVA_HOME
    os.environ["PATH"] = JAVA_HOME + "/bin" + os.pathsep + os.environ["PATH"]
