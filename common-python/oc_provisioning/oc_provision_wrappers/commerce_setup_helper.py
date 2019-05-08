# The MIT License (MIT)
#
# Copyright (c) 2018 Oracle
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
__copyright__ = "Copyright (c) 2018  Oracle and/or its affiliates. All rights reserved."
__credits__ ="Hadi Javaherian (Oracle IaaS and App Dev Team)"
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import ConfigParser
#import configparser
import fileinput
import json
import os
import platform
import shutil
from subprocess import Popen, PIPE, STDOUT
import urllib2
import logging

logger = logging.getLogger(__name__)


def find_default_machine(configData, full_path):

     #managed_key_mserver = "WEBLOGIC_managed_servers"
    managed_key_machine = "WEBLOGIC_machines"

    if  managed_key_machine in configData:
        #jsonDataArray_mserver = configData[managed_key_mserver]
        jsonDataArray_machine = configData[managed_key_machine]
    else:
        logging.error(jsonDataArray_machine + " is missing from json. will not retrieve hostname")
        return ''

    logging.info("retrieving host name")


    for jsonData_machine in jsonDataArray_machine:
        requiredFields = ['machineName', 'machineAddress']
        check_required_fields(jsonData_machine, requiredFields)

    return jsonDataArray_machine 

    raise ValueError ("Required field missing from json")


def find_host_from_machine(machine_name, configData, full_path):
    """
    find the host name from the machine name 
    """     
    #managed_key_mserver = "WEBLOGIC_managed_servers"
    managed_key_machine = "WEBLOGIC_machines"

    if  managed_key_machine in configData:
        #jsonDataArray_mserver = configData[managed_key_mserver]
        jsonDataArray_machine = configData[managed_key_machine]
    else:
        logging.error(jsonDataArray_machine + " is missing from json. will not retrieve hostname")
        return ''
    
    logging.info("retrieving host name")

    #for jsonData_mserver in jsonDataArray_mserver:             
    #    requiredFields = ['managedServerHost']
    #    commerce_setup_helper.check_required_fields(jsonData_mserver, requiredFields)
    
    #    WL_SERVER_HOST = jsonData['managedServerHost'] 


    for jsonData_machine in jsonDataArray_machine:             
        requiredFields = ['machineName', 'machineAddress']
        check_required_fields(jsonData_machine, requiredFields)
    
        WL_MACHINE_NAME = jsonData_machine['machineName']
        WL_MACHINE_ADDR = jsonData_machine['machineAddress']    

        if (machine_name == WL_MACHINE_NAME):
           logging.info("found host name:  " + WL_MACHINE_ADDR)

           return WL_MACHINE_ADDR

    raise ValueError ("Required field " + machine_name+ " missing from json")

def load_json_from_url(jsonUrl, key):
    """
    Read json data from a URL
    """      
    try:
        data = urllib2.urlopen(jsonUrl)
    except urllib2.URLError, e:
        logger.error("url error")
    jsonData = json.load(data)
    if key not in jsonData:
        raise ValueError ("Root " + key + " item missing")   
    return jsonData[key]

def load_json_from_file(jsonFile, key):
    """
    Read json data from a file on the filesystem
    """        
    logger.info("trying to load json from file...."+ jsonFile + "  and key: " + key)
    with open(jsonFile) as data_file:    
        logger.info("opening the file now.....")
        data = json.load(data_file)
        logger.info("done opening the file.....")
        if key not in data:
            raise ValueError ("Root " + key + " item missing")   

        logger.info("returning the key.....")
        return data[key]
       
def check_required_fields(jsonData, requiredFields):
    """
    check for all requiredFields in jsonData
    """     
    for field in requiredFields:
        logger.info("checking for requiredFields:  \n" + field)
        if field not in jsonData:
            raise ValueError ("Required field " + field + " missing from json")

def callPopenDefaultShell(command):
    """
    call external process
    """
    logger.info("About to call Popen with False Shell......")
    proc = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    logger.info("Just called the Popen......")

    out, err = proc.communicate()
    if out:
        logger.info(out)
    if err:
        logger.info("we ran into an err here......")
        logger.error(err)

    logger.info("proc is returning ......")

    return proc.returncode

 

def callPopen(command):
    """
    call external process
    """       
    proc = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    out, err = proc.communicate()
    if out:
        logger.info(out)
    if err:
        logger.error(err)  
    
    return proc.returncode

def substitute_file_fields_inplace(infile, replacement_dict):
    """
    Read infile. Replace any string occurrences in replacement_dict. Write result back to infile
    """      
    indata = open(infile).read()
    outdata = open(infile, 'w')
    if replacement_dict is not None:
        for i in replacement_dict.keys():
            indata = indata.replace(i, replacement_dict[i])
    outdata.write(indata)
    outdata.close 
    
            
def substitute_file_fields(infile, outfile, replacement_dict):
    """
    Read infile. Replace any string occurrences in replacement_dict. Write result to outfile
    """      
    indata = open(infile).read()
    outdata = open(outfile, 'w')
    if replacement_dict is not None:
        for i in replacement_dict.keys():
            indata = indata.replace(i, replacement_dict[i])
    outdata.write(indata)
    outdata.close 
    
def change_file_owner(file_name, user, group):
    """
    Change file owner and group
    """         
    command = "chown " + user + ":" + group + " " + file_name
    callPopen(command)  

    
def mkdir_with_perms(path, owner, group):
    """
    Make recursive directories, setting ownership along the way
    """
    # check if the entire path already exists
    if (os.path.exists(path)):
        # take ownership
        change_file_owner(path, owner, group)
    else:    
        path = path[1:]
        dirs = path.split("/")
        dirToMake = ''
        for mydir in dirs:
            dirToMake += '/' + mydir
            if not (os.path.exists(dirToMake)):
                mk_cmd = "mkdir " + dirToMake
                callPopen(mk_cmd) 
                change_file_owner(dirToMake, owner, group)

def add_to_bashrc(user, text):
    """
    Add text to a users .bashrc file
    """        
    homeDir = os.path.expanduser("~" + user)
    bashrc_file = homeDir + "/.bashrc"
    with open(bashrc_file, "a") as myfile:
        myfile.write(text)
    myfile.close()

def exec_cmd_default (command):
    """
    Exec command as the user who called this function
    """
    logger.info("exec_cmd is running in the uefault shell: " + command)
    returncode = callPopenDefaultShell(command)
    logger.info("exec_cmd default shell just ended......")
    return returncode


def exec_cmd (command): 
    """
    Exec command as the user who called this function
    """        
    logger.info("exec_cmd is " + command)
    returncode = callPopen(command)
    return returncode

        
def exec_as_user (user, command):
    """
    Exec a command as another user
    """        
    COMMAND_PREFIX = "su - " + user + " -c "
    exec_cmd = COMMAND_PREFIX + command
    logger.info("exec_as_user cmd is " + exec_cmd)
    returncode = callPopen(exec_cmd)
    return returncode
            
def copy_start_script (startOnBoot, srcFile, field_replacement, dstFile=None):
    """
    Copy init scripts to /etc/init.d, and link to run on boot if startOnBoot true
    """        
    outDir = "/etc/init.d"
    path, filename = os.path.split(srcFile)
    if dstFile is None:
        outFilename = filename.replace('.master', '')
    else:
        outFilename = dstFile
        
    outFile = outDir + "/" + outFilename
    substitute_file_fields(srcFile, outFile, field_replacement)
    os.chmod(outFile, 0755)
    if (startOnBoot == 'true'):
        # solaris does not use chkconfig. add to rc dirs manually
        if (platform.system() == 'SunOS'):
            startLinkCommand = "ln -s " + outFile + " /etc/rc3.d/S99" + outFilename   
            stopLinkCommand = "ln -s " + outFile + " /etc/rc2.d/K74" + outFilename
            exec_cmd(startLinkCommand)
            exec_cmd(stopLinkCommand)
        else:
            chkCmd = "chkconfig --add " + outFilename
            exec_cmd(chkCmd)            

def copy_start_script_home (user, group, srcFile, field_replacement):
    """
    Copy init scripts to users bin directory
    """        
    homeDir = os.path.expanduser("~" + user)
    binDir = homeDir + "/bin"
    if not (os.path.exists(binDir)):
        os.mkdir(binDir, 0755)
        change_file_owner(binDir, user, group)
    path, filename = os.path.split(srcFile)
    outFile = binDir + "/" + filename.replace('.master', '')
    substitute_file_fields(srcFile, outFile, field_replacement)
    os.chmod(outFile, 0755)
    change_file_owner(outFile, user, group)
    
def copy_sshkeys(fromUser, toUser, toUserGroup):
    """
    Sync up ssh authorized_keys from one user to another
    """      
    fromHomeDir = os.path.expanduser("~" + fromUser) + "/.ssh"
    toHomeDir = os.path.expanduser("~" + toUser) + "/.ssh"
    if not (os.path.exists(toHomeDir)):
        os.mkdir(toHomeDir, 0700)
    shutil.copyfile(fromHomeDir + "/authorized_keys" , toHomeDir + "/authorized_keys")
    os.chmod(toHomeDir + "/authorized_keys", 0644)
    change_file_owner(toHomeDir + "/authorized_keys", toUser, toUserGroup)
    
def get_path_to_binary(prop_key):
    """
    Get the path to a product binary from properties file
    """      
    config = ConfigParser.ConfigParser()
    installer_properties = "installer.properties"
    installer_section = "installers"
    config.read(installer_properties)
    return config.get(installer_section, prop_key)
    
