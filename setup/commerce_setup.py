#!/usr/bin/python2.7

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

import getopt
import os
from pprint import pprint
import sys
from urlparse import urlparse
import traceback

from oc_provision_wrappers import commerce_setup_helper 
from oc_provision_wrappers import load_user_metadata
from oc_provision_wrappers.sshkeys import copy_ssh_keys_helper
from oc_provision_wrappers.storage import advanced_storage_helper
from oc_provision_wrappers.storage import storage_helper
from oc_provision_wrappers import setup_logger
from oc_provision_wrappers import version_coordinator

sys.path.insert(0, os.path.abspath(".."))

full_path = os.path.dirname(os.path.abspath(__file__))

# root key to get from our datasource
root_json_key = 'commerceSetup' 

# url for OPC user-data
user_data_url = "http://192.0.0.192/latest/user-data"

# url for OpenStack user-data
os_user_data_url = "http://169.254.169.254/latest/user-data"

json_ds = None
install_java = None
install_atg = None
install_atgpatch = None
install_mdex = None
install_platform = None
install_tools = None
install_cas = None
install_otd = None
config_otd = None
copy_ssh_keys = None
add_storage = None
advanced_storage = None
install_weblogic = None
managed_wl_server = None
create_wl_domain = None
config_wl_domain = None
config_wl_ds = None
create_wl_servers = None
create_wl_machines = None
create_wl_bootfiles = None
pack_wl_domain = None
install_oracle_db = None
showDebug = None
isOpenstack = None
weblogic_version = None
atg_version = None
endeca_version = None
otd_version = None
database_version = None
java_version = None


try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['java', 'addstorage', 'advancedStorage', 'weblogic', 'weblogicDomain', 'weblogicBootFiles', 'weblogicManagedServer',
                                                  'weblogicPackDomain', 'weblogicSettings', "weblogicDatasources", 'weblogicServers', 'weblogicMachines', 'atg', 'atgpatch',
                                                  'mdex', 'platformServices', 'toolsAndFramework', 'cas', 'endeca', 'dgraph', 'otdInstall', 'otdConfig',
                                                  'copy-ssh-keys', 'db', 'debug', 'openstack', 'configSource='])
except getopt.GetoptError as err:
    print "Argument error", err
    sys.exit(2)

for opt, arg in opts:
    if opt in ('--mdex', '--endeca', '--dgraph'):
        install_mdex = True        
    if opt in ('--platformServices', '--endeca', '--dgraph'):
        install_platform = True        
    if opt in ('--toolsAndFramework', '--endeca'):
        install_tools = True        
    if opt in ('--cas', '--endeca'):
        install_cas = True        
    if opt == '--java':
        install_java = True        
    if opt == '--atg':
        install_atg = True  
    if opt == '--atgpatch':
        install_atgpatch = True                  
    if opt == '--otdInstall':
        install_otd = True
    if opt == '--otdConfig':
        config_otd = True   
    if opt == '--copy-ssh-keys':
        copy_ssh_keys = True 
    if opt == '--addstorage':
        add_storage = True
    if opt == '--advancedStorage':
        advanced_storage = True        
    if opt == '--weblogic':
        install_weblogic = True
    if opt == '--weblogicManagedServer':
        managed_wl_server = True        
    if opt == '--weblogicDomain':
        create_wl_domain = True   
    if opt == '--weblogicPackDomain':
        pack_wl_domain = True                  
    if opt == '--weblogicSettings':
        config_wl_domain = True
    if opt == '--weblogicDatasources':
        config_wl_ds = True          
    if opt == '--weblogicServers':
        create_wl_servers = True
    if opt == '--weblogicMachines':
        create_wl_machines = True
    if opt == '--weblogicBootFiles':
        create_wl_bootfiles = True        
    if opt == '--db':
        install_oracle_db = True
    if opt == '--openstack':
        isOpenstack = True        
    if opt == '--debug':
        showDebug = True                                                                                              
    if opt == '--configSource':
        json_ds = arg
        
  
configData = None

logger = setup_logger.setup_shared_logger('')

# decide where to load our JSON data from
if json_ds == None:
    logger.info("using default json configs ")
    json_ds = full_path + '/defaultJson/defaultConfig.json'
    configData = commerce_setup_helper.load_json_from_file(json_ds, root_json_key) 
elif json_ds == "user-data":
    logger.info("loading json from user metadata")
    if (isOpenstack):
        configData = load_user_metadata.load_os_user_metadata(os_user_data_url, root_json_key)
    else:
        configData = load_user_metadata.load_user_metadata(user_data_url, root_json_key)
elif json_ds.startswith('file'):
    logger.info("checking for file based json data from " + json_ds)
    junk, filename = json_ds.split(":")
    file_ds = full_path + '/defaultJson/' + filename
    if os.path.isfile(file_ds):
        configData = commerce_setup_helper.load_json_from_file(file_ds, root_json_key) 
else:
    test_for_url = urlparse(json_ds)
    isUrl = bool(test_for_url.scheme)
    if isUrl: 
        logger.info("loading json from external URL " + json_ds)
        configData = commerce_setup_helper.load_json_from_url(json_ds, root_json_key)
    else:
        logger.error("json source is not a URL")

if configData == None:
    logger.error("no configuration data could be loading. Exiting")
    sys.exit()

if showDebug:
    print 'ARGV      :', sys.argv[1:]
    pprint (configData)
    
install_versions = commerce_setup_helper.get_json_key(configData, 'install_versions')

# get product versions to install from json
if 'weblogic' in install_versions:
    weblogic_version = install_versions['weblogic']
if 'endeca' in install_versions:
    endeca_version = install_versions['endeca']
if 'atg' in install_versions:
    atg_version = install_versions['atg']
if 'otd' in install_versions:
    otd_version = install_versions['otd']
if 'database' in install_versions:
    database_version = install_versions['database']
if 'java' in install_versions:
    java_version = install_versions['java']

if copy_ssh_keys:
    try:
        copy_ssh_keys_helper.copy_keys(configData, full_path)
    except:
        traceback.print_exc()
        pass    
    
if add_storage:
    try:
        storage_helper.mount_storage(configData, full_path)
    except:
        traceback.print_exc()
        pass    

if advanced_storage:
    try:
        advanced_storage_helper.advanced_storage(configData, full_path)
    except:
        traceback.print_exc()
        pass    
       
if install_java:
    try:
        version_coordinator.install_java(configData, full_path)
    except:
        traceback.print_exc()
        pass    

if install_weblogic:
    try:  
        version_coordinator.install_weblogic(configData, full_path)       
    except:
        traceback.print_exc()
        pass    
        
if create_wl_domain:
    try:
        version_coordinator.create_wl_domain(configData, full_path)    
        # weblogic_domain_config.create_wl_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass         
    
if config_wl_domain: 
    try:
        version_coordinator.config_wl_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass    
    
if config_wl_ds:
    try:
        version_coordinator.config_wl_ds(configData, full_path)
    except:
        traceback.print_exc()
        pass           
     
if create_wl_machines:
    try:
        # for adding to already running domain
        version_coordinator.create_wl_machines(configData, full_path)
    except:
        traceback.print_exc()
        pass      
    
if create_wl_servers:
    try:
        # for adding to already running domain
        version_coordinator.create_wl_servers(configData, full_path)
    except:
        traceback.print_exc()
        pass      

if pack_wl_domain:
    try:
        version_coordinator.pack_wl_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass     
    
if managed_wl_server:
    try:
        version_coordinator.managed_wl_server(configData, full_path)
    except:
        traceback.print_exc()
        pass    
    
if create_wl_bootfiles:
    try:
        version_coordinator.create_wl_bootfiles(configData, full_path)
    except:
        traceback.print_exc()
        pass     
    
if managed_wl_server or create_wl_domain:
    try:
        # keep this after boot files. Without them, instances won't start
        version_coordinator.managed_scripts(configData, full_path)
    except:
        traceback.print_exc()
        pass         
                
if install_atg:
    try:
        version_coordinator.install_atg(configData, full_path)
    except:
        traceback.print_exc()
        pass
    
if install_atgpatch:
    try:
        version_coordinator.install_atgpatch(configData, full_path)
    except:
        traceback.print_exc()
        pass         
            
if install_mdex:
    try:
        version_coordinator.install_mdex(configData, full_path)
    except:
        traceback.print_exc()
        pass    
    
if install_platform:
    try:
        version_coordinator.install_platformServices(configData, full_path)
    except:
        traceback.print_exc()
        pass

if install_tools:
    try:
        version_coordinator.install_toolsAndFramework(configData, full_path)    
    except:
        traceback.print_exc()
        pass    
    
if install_cas:
    try:
        version_coordinator.install_cas(configData, full_path)
    except:
        traceback.print_exc()
        pass    
    
if install_otd:
    try:
        version_coordinator.install_otd(configData, full_path)
    except:
        traceback.print_exc()
        pass    

if config_otd:
    try:
        version_coordinator.config_otd(configData, full_path) 
    except:
        traceback.print_exc()
        pass

if install_oracle_db:
    try:
        #oracle_rdbms_install.install_oracle(configData, full_path)
        version_coordinator.install_oracle_db(configData, full_path)
    except:
        traceback.print_exc()
        pass    

logger.info("Setup Complete")     
