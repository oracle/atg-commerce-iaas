#!/usr/bin/python2.7

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
__version__ = "1.0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import getopt
import os
from pprint import pprint
import sys
from urlparse import urlparse
import traceback

from oc_provision_wrappers import commerce_setup_helper 
from oc_provision_wrappers import load_user_metadata
from oc_provision_wrappers.atg import create_atg_server_layers 
from oc_provision_wrappers.atg.v11_3 import atg_helper
from oc_provision_wrappers.atg.v11_3 import atgpatch_helper
from oc_provision_wrappers.atg.v11_3 import cim_setup_helper
from oc_provision_wrappers.database.v12c import create_atg_schema
from oc_provision_wrappers.database.v12c import oracle_pdb_connect
from oc_provision_wrappers.database.v12c import oracle_rdbms_install
from oc_provision_wrappers.endeca.v11_3 import cas_helper
from oc_provision_wrappers.endeca.v11_3 import mdex_helper
from oc_provision_wrappers.endeca.v11_3 import platform_helper
from oc_provision_wrappers.endeca.v11_3 import tools_helper
from oc_provision_wrappers.java import java8_helper
from oc_provision_wrappers.java import java_generic
from oc_provision_wrappers.otd.v11_1 import otd_config
from oc_provision_wrappers.otd.v11_1 import otd_helper
from oc_provision_wrappers.sshkeys import copy_ssh_keys_helper
from oc_provision_wrappers.storage import advanced_storage_helper
from oc_provision_wrappers.storage import storage_helper
from oc_provision_wrappers.wls.v12_2_1 import weblogic_create_datasources    
from oc_provision_wrappers.wls.v12_2_1 import weblogic_create_dbaas_datasources
from oc_provision_wrappers.wls.v12_2_1 import weblogic_create_machine
from oc_provision_wrappers.wls.v12_2_1 import weblogic_create_managed_server
from oc_provision_wrappers.wls.v12_2_1 import weblogic_domain_config
from oc_provision_wrappers.wls.v12_2_1 import weblogic_domain_settings
from oc_provision_wrappers.wls.v12_2_1 import weblogic_helper
from oc_provision_wrappers.wls.v12_2_1 import weblogic_install_managed_server
from oc_provision_wrappers.wls.v12_2_1 import weblogic_packer
from oc_provision_wrappers.wls import weblogic_boot_properties
from oc_provision_wrappers.wls import weblogic_create_managed_scripts
from oc_provision_wrappers import setup_logger

import logging


logger = logging.getLogger(__name__)


sys.path.insert(0, os.path.abspath(".."))

full_path = os.path.dirname(os.path.abspath(__file__))

# root key to get from our datasource
root_json_key = 'commerceSetup' 

# url for user-data
user_data_url = "http://192.0.0.192/latest/user-data"

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
config_wl_dbaas_ds = None
create_wl_servers = None
create_wl_machines = None
create_wl_bootfiles = None
pack_wl_domain = None
install_oracle_db = None
showDebug = None
install_crs_store = None
cim_batch_file = None
testing = None



try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['java', 'addstorage', 'advancedStorage', 'weblogic', 'weblogicDomain', 'weblogicBootFiles', 'weblogicManagedServer',
                                                  'weblogicPackDomain', 'weblogicSettings', 'weblogicDatasources', 'weblogicDBaaSDatasources', 'weblogicServers', 'weblogicMachines', 'atg', 'atgpatch',
                                                  'mdex', 'platformServices', 'toolsAndFramework', 'cas', 'endeca', 'dgraph', 'otdInstall', 'otdConfig',
                                                  'copy-ssh-keys', 'db', 'debug', 'configSource=', 'crs', 'atest'])

except getopt.GetoptError as err:
    print "Argument error", err
    sys.exit(2)

logger.info("looking for the correct args.....")

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
        config_wl_dbaas_ds = False
        config_wl_ds = True            
    if opt == '--weblogicDBaaSDatasources':
        config_wl_ds = False
        config_wl_dbaas_ds = True
        root_cim_json_key = 'CIMSetup'
    if opt == '--weblogicServers':
        create_wl_servers = True
    if opt == '--weblogicMachines':
        create_wl_machines = True
    if opt == '--weblogicBootFiles':
        create_wl_bootfiles = True        
    if opt == '--db':
        install_oracle_db = True
    if opt == '--debug':
        showDebug = True                                                                                              
    if opt == '--configSource':
        json_ds = arg
    if opt == '--crs':
        install_crs_store = True
    if opt == '--atest':
        testing = True
        
    # else:
    #    sys.exit(2)

configData = None
configCIMData = None

logger = setup_logger.setup_shared_logger('')


def crs_configuration(full_path):
    logger.info("reading the crs files \n")
    json_cim_ds = full_path + '/crsJson/CIM_113_template.json'
    batchFile = full_path + '/crsJson/atg113crsTemplate-v1_converted.cim'
    json_ds = full_path + '/crsJson/crsConfig.json'
    root_json_key = 'commerceCRSSetup'
    root_cim_json_key = 'CIMSetup'

    logger.info("the full path with json_ds: " + json_ds)

    #testing
    logger.info("testing the crs_configuration method.....now exiting.................. \n")

    configData = commerce_setup_helper.load_json_from_file(json_ds, root_json_key)

    configCIMData = commerce_setup_helper.load_json_from_file(json_cim_ds, root_cim_json_key)

    logger.info("setup the ATG schema in DBaaS..")
    
    logger.info("Now we start instlling the components...")
 
    if showDebug:
        print 'ARGV      :', sys.argv[1:]
        pprint (configData)

    try:
        #java8_helper.install_java(configData, full_path)
        #take out the comment
        java_generic.install_java(configData, full_path)
    except:
        traceback.print_exc()
        pass

    try:
        mdex_helper.install_mdex(configData, full_path)
    except:
        traceback.print_exc()
        pass

    try:
        platform_helper.install_platformServices(configData, full_path)
    except:
        traceback.print_exc()
        pass

    try:
        tools_helper.install_toolsAndFramework(configData, full_path)
    except:
        traceback.print_exc()
        pass

    try:
        cas_helper.install_cas(configData, full_path)
    except:
        traceback.print_exc()
        pass

    try:
        logger.info("*********************************  --weblogic  ********************* \n")
        weblogic_helper.install_weblogic(configData, full_path)
    except:
        traceback.print_exc()
        pass

    try:
        logger.info("*********************************  --weblogicDomain  ********************* \n")
        weblogic_domain_config.create_wl_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass

    
    try:
        atg_helper.install_atg(configData, full_path)
        # This may be useful as its own option in the future. Leave here w/ATG install for now
        create_atg_server_layers.generate_atg_server_layers(configData, full_path)
    except:
        traceback.print_exc()
        pass

    if install_atgpatch:
        try:
            atgpatch_helper.install_atgpatch(configData, full_path)
        except:
            traceback.print_exc()
        pass

    try:
        create_atg_schema.schema_definition(configCIMData, full_path)
    except:
        traceback.print_exc()
        pass
 
    try:
        logger.info("Calling pre_cim_setup.....")
        cim_setup_helper.pre_cim_setup(configData, full_path)
        logger.info("Calling config_cim.....")
        cim_setup_helper.config_cim(batchFile, configData, configCIMData, full_path)
        logger.info("Calling exec_cim_batch.....")
        cim_setup_helper.exec_cim_batch(batchFile, configCIMData, full_path)
        logger.info("Just created the CIM file..now running post cim configs....")
        cim_setup_helper.post_cim_setup(configData, full_path)
        logger.info("config_cim is Done.....")
        #alterh the epub tables here
        create_atg_schema.alter_pub_table(configCIMData, full_path)
        logger.info("Done altering ebpub table.....")
    except:
        traceback.print_exc()
        pass

    logger.info("CRS Setup Complete")


if json_ds == None:
    logger.info("using default json configs \n")
    json_ds = full_path + '/defaultJson/defaultConfig.json'

    #testing
    logger.info("testing the null or any other args....now exiting.................. \n")
    #sys.exit()

    configData = commerce_setup_helper.load_json_from_file(json_ds, root_json_key) 

    #Here we also load the CIM config file to get the datasource information for the weblogic datasources
    if (config_wl_dbaas_ds):
        #in this case we have both configData and configCIMData
        json_ds = full_path + '/crsJson/CIM_113_template.json'
        configCIMData = commerce_setup_helper.load_json_from_file(json_ds, root_cim_json_key)

elif json_ds == "user-data":
    logger.info("loading json from user metadata")

    #testing
    logger.info("testing the user-data.....now exiting.................. \n")
    sys.exit()

    configData = load_user_metadata.load_user_metadata(user_data_url, root_json_key)
elif json_ds.startswith('file'):
    logger.info("checking for file based json data")
    junk, filename = json_ds.split(":")
    file_ds = full_path + '/defaultJson/' + filename

    #testing
    logger.info("testing the file:.....now exiting.................. \n")
    sys.exit()
    
    if os.path.isfile(file_ds):
        configData = commerce_setup_helper.load_json_from_file(file_ds, root_json_key)     
else:
    test_for_url = urlparse(json_ds)
    isUrl = bool(test_for_url.scheme)

    #testing
    logger.info("testing the else condition.....now exiting.................. \n")
    sys.exit()    

    if isUrl: 
        logger.info("loading json from external URL")
        configData = commerce_setup_helper.load_json_from_url(json_ds, root_json_key)    

if (configCIMData == None and configData == None):
    logger.error("no configution data could be loading. Exiting")
    sys.exit()


#first test is for the crs
if install_crs_store:
    logger.info("we are using the crs config files \n")

    install_java = False
    install_atg = False
    install_mdex = False
    install_platform = False
    install_tools = False
    install_cas = False
    install_otd = False
    config_otd = False
    copy_ssh_keys = False
    add_storage = False
    advanced_storage = False
    install_weblogic = False
    managed_wl_server = False
    create_wl_domain = False
    config_wl_domain = False
    config_wl_ds = False
    create_wl_servers = False
    create_wl_machines = False
    create_wl_bootfiles = False
    pack_wl_domain = False
    install_oracle_db = False
    install_atgpatch = False
    showDebug = False
    install_crs_store = True
    testing = False

    try:
        crs_configuration(full_path)
        logger.info("we have read the data with the key......")
    except:
        traceback.print_exc()
        pass


if showDebug:
    print 'ARGV      :', sys.argv[1:]
    pprint (configData)

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
        #java8_helper.install_java(configData, full_path)  
        java_generic.install_java(configData, full_path)
    except:
        traceback.print_exc()
        pass
    
if install_weblogic:
    try:
        logger.info("*********************************  --weblogic  ********************* \n")
        weblogic_helper.install_weblogic(configData, full_path)
    except:
        traceback.print_exc()
        pass    
        
if create_wl_domain:
    try:
        logger.info("*********************************  --weblogicDomain  ********************* \n")
        weblogic_domain_config.create_wl_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass         
    
if config_wl_domain:
    try:
        logger.info("*********************************  --weblogicSettings  ********************* \n")
        weblogic_domain_settings.config_wl_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass    
    
if config_wl_ds:
    config_wl_dbaas_ds = False
    logger.info("We are configuring the WLS datasources for IaaS \n")
    sys.exit()
    try:
        weblogic_create_datasources.config_wl_datasources(configData, full_path)
    except:
        traceback.print_exc()
        pass           

if config_wl_dbaas_ds:
    config_wl_ds = False
    logger.info("We are configuring the WLS datasources for DBaaS \n")
    #sys.exit()
    try:
        weblogic_create_dbaas_datasources.config_wl_dbaas__datasources(configData, configCIMData, full_path)
    except:
        traceback.print_exc()
        pass
     
if create_wl_machines:
    try:
        logger.info("*********************************  --weblogicMachines  ********************* \n")
        # for adding to already running domain
        weblogic_create_machine.create_machines(configData, full_path)
    except:
        traceback.print_exc()
        pass      
    
if create_wl_servers:
    try:
        logger.info("*********************************  --weblogicServers  ********************* \n")
        # for adding to already running domain
        weblogic_create_managed_server.create_servers(configData, full_path)
    except:
        traceback.print_exc()
        pass      

if pack_wl_domain:
    try:
        logger.info("*********************************  --weblogicPackDomain  ********************* \n")
        weblogic_packer.pack_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass     
    
if managed_wl_server:
    try:
        logger.info("*********************************  --weblogicManagedServer  ********************* \n")
        weblogic_install_managed_server.unpack_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass

if create_wl_bootfiles:
    try:
        logger.info("*********************************  --weblogicBootFiles  ********************* \n")
        weblogic_boot_properties.create_boot_properties(configData, full_path)
    except:
        traceback.print_exc()
        pass   

if managed_wl_server or create_wl_domain:
    try:
        # keep this after boot files. Without them, instances won't start
        weblogic_create_managed_scripts.create_managed_scripts(configData, full_path)
    except:
        traceback.print_exc()
        pass  
                       
if install_atg:
    try:
        atg_helper.install_atg(configData, full_path)
        # This may be useful as its own option in the future. Leave here w/ATG install for now
        create_atg_server_layers.generate_atg_server_layers(configData, full_path)
    except:
        traceback.print_exc()
        pass

if install_atgpatch:
    try:
        atgpatch_helper.install_atgpatch(configData, full_path) 
    except:
        traceback.print_exc()
        pass         
            
if install_mdex:
    try:
        mdex_helper.install_mdex(configData, full_path)
    except:
        traceback.print_exc()
        pass
    
if install_platform:
    try:
        platform_helper.install_platformServices(configData, full_path)
    except:
        traceback.print_exc()
        pass    

if install_tools:
    try:
        tools_helper.install_toolsAndFramework(configData, full_path)    
    except:
        traceback.print_exc()
        pass    
    
if install_cas:
    try:
        cas_helper.install_cas(configData, full_path)
    except:
        traceback.print_exc()
        pass    
    
if install_otd:
    try:
        otd_helper.install_otd(configData, full_path)
    except:
        traceback.print_exc()
        pass    

if config_otd:
    try:
        otd_config.config_otd(configData, full_path) 
    except:
        traceback.print_exc()
        pass         

if install_oracle_db:
    try:
        oracle_rdbms_install.install_oracle(configData, full_path)
    except:
        traceback.print_exc()
        pass    

if testing:
   logger.info("This is ONLY a test.....")
   logger.info("Testing begins.....")

   configCIMData = commerce_setup_helper.load_json_from_file('/opt/oracle/install/11.3/crsJson/CIM_113_template.json', 'CIMSetup')
   full_path = '/opt/oracle/install/11.3'

   configData = commerce_setup_helper.load_json_from_file('/opt/oracle/install/11.3/crsJson/crsConfig.json', 'commerceCRSSetup')

   #batchFile = full_path + '/crsJson/atg113crsTemplate-v1_converted.cim'
   batchFile = full_path + '/crsJson/test.cim'
#   try:
#      create_atg_schema.schema_definition(configCIMData, full_path)
#   except:
#      traceback.print_exc()
#      pass

   try:
      #logger.info("Calling pre_cim_setup.....")
      #cim_setup_helper.pre_cim_setup(configData, full_path)
      #logger.info("Calling config_cim.....")
      #cim_setup_helper.config_cim(batchFile, configData, configCIMData, full_path)
      #logger.info("cim file created.....")
      logger.info("Calling exec_cim_batch.....")
      cim_setup_helper.exec_cim_batch(batchFile, configData, full_path)
      logger.info("Just created the CIM file....about to do the post cim configs..")
      #cim_setup_helper.post_cim_setup(configData, full_path)
      #logger.info("config_cim testing is Done.....")
      #alter the epub tables here
      #create_atg_schema.alter_pub_table(configCIMData, full_path)
      #logger.info("Done altering ebpub table.....")
   except:
      traceback.print_exc()
      pass

 
   logger.info("Testing ends.....")

logger.info("Setup Complete")      
