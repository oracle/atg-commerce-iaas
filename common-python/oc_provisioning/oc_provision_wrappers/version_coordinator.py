#!/usr/bin/python2.7

# The MIT License (MIT)
#
# Copyright (c) 2017 Oracle
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
from oc_provision_wrappers.wls.v12c import weblogic_helper
from oc_provision_wrappers.wls.v12c import weblogic_boot_properties
from oc_provision_wrappers.wls.v12c import weblogic_create_managed_scripts
from oc_provision_wrappers.java import java_generic
from oc_provision_wrappers.atg import create_atg_server_layers

import traceback
import importlib
import logging

logger = logging.getLogger(__name__)

wl_modules = None
endeca_modules = None
atg_modules = None
db_modules = None
otd_modules = None


def _set_product_versions(configData):
    install_versions = commerce_setup_helper.get_json_key(configData, 'install_versions')
    
    # get product versions to install from json
    if 'weblogic' in install_versions:
        weblogic_version = install_versions['weblogic']
        weblogic_version = weblogic_version.replace(".","_")
        wlmod = "oc_provision_wrappers.wls.v" + weblogic_version
        global wl_modules
        #wl_modules = importlib.import_module(wlmod)
        wl_modules = wlmod        
    if 'endeca' in install_versions:
        endeca_version = install_versions['endeca']
        endeca_version = endeca_version.replace(".","_")
        endecamod = "oc_provision_wrappers.endeca.v" + endeca_version
        global endeca_modules
        endeca_modules = endecamod
    if 'atg' in install_versions:
        atg_version = install_versions['atg']
        atg_version = atg_version.replace(".","_")
        atgmod = "oc_provision_wrappers.atg.v" + atg_version
        global atg_modules
        atg_modules = atgmod       
    if 'otd' in install_versions:
        otd_version = install_versions['otd']
        otd_version = otd_version.replace(".","_")
        otdmod = "oc_provision_wrappers.otd.v" + otd_version
        global otd_modules
        otd_modules = otdmod
                 
    if 'database' in install_versions:
        database_version = install_versions['database']
        database_version = database_version.replace(".","_")
        dbmod = "oc_provision_wrappers.database.v" + database_version
        global db_modules
        db_modules = dbmod
           
    if 'java' in install_versions:
        java_version = install_versions['java']            
                 
    
def install_weblogic(configData, full_path):
    try:
        weblogic_helper.install_weblogic(configData, full_path)       
    except:
        traceback.print_exc()
        pass     

def create_wl_domain(configData, full_path):
    try:
        _set_product_versions(configData)
        
        mymod = importlib.import_module(wl_modules+'.weblogic_domain_config')
        mymod.create_wl_domain(configData, full_path)

    except:
        traceback.print_exc()
        pass

def config_wl_domain(configData, full_path):
    try:
        _set_product_versions(configData)
        
        mymod = importlib.import_module(wl_modules+'.weblogic_domain_settings')
        mymod.config_wl_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass        

def config_wl_ds(configData, full_path):
    try:
        _set_product_versions(configData)
        
        mymod = importlib.import_module(wl_modules+'.weblogic_create_datasources')
        mymod.config_wl_datasources(configData, full_path)
    except:
        traceback.print_exc()
        pass           
     
def create_wl_machines(configData, full_path):
    try:
        _set_product_versions(configData)
        
        mymod = importlib.import_module(wl_modules+'.weblogic_create_machine')
        # for adding to already running domain
        mymod.create_machines(configData, full_path)
    except:
        traceback.print_exc()
        pass      
    
def create_wl_servers(configData, full_path):
    try:
        _set_product_versions(configData)
        
        mymod = importlib.import_module(wl_modules+'.weblogic_create_managed_server')
        # for adding to already running domain
        mymod.create_servers(configData, full_path)
    except:
        traceback.print_exc()
        pass      

def pack_wl_domain(configData, full_path):
    try:
        _set_product_versions(configData)
        
        mymod = importlib.import_module(wl_modules+'.weblogic_packer')
        mymod.pack_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass     
    
def managed_wl_server(configData, full_path):
    try:
        _set_product_versions(configData)
        
        mymod = importlib.import_module(wl_modules+'.weblogic_install_managed_server')
        mymod.unpack_domain(configData, full_path)
    except:
        traceback.print_exc()
        pass    
    
def create_wl_bootfiles(configData, full_path):
    try:
        weblogic_boot_properties.create_boot_properties(configData, full_path)
    except:
        traceback.print_exc()
        pass     
    
def managed_scripts(configData, full_path):
    try:
        # keep this after boot files. Without them, instances won't start
        weblogic_create_managed_scripts.create_managed_scripts(configData, full_path)
    except:
        traceback.print_exc()
        pass         
        
def install_java(configData, full_path):
    try:
        _set_product_versions(configData)
        java_generic.install_java(configData, full_path)
    except:
        traceback.print_exc()
        pass         
    
def install_otd(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(otd_modules+'.otd_helper')
        mymod.install_otd(configData, full_path)                
    except:
        traceback.print_exc()
        pass    

def config_otd(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(otd_modules+'.otd_config')
        mymod.config_otd(configData, full_path)        
    except:
        traceback.print_exc()
        pass     

def install_atg(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(atg_modules+'.atg_helper')
        mymod.install_atg(configData, full_path)         
       
        # This may be useful as its own option in the future. Leave here w/ATG install for now
        create_atg_server_layers.generate_atg_server_layers(configData, full_path)
    except:
        traceback.print_exc()
        pass
    
def install_atgpatch(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(atg_modules+'.atgpatch_helper')
        success = mymod.install_atgpatch(configData, full_path) 
                
        # fix issues in the patch
        if (success):
            mymod = importlib.import_module(atg_modules+'.atgpatch_postinstall')
            mymod.post_install_cmds(configData, full_path)            
            #atg_modules.atgpatch_postinstall.post_install_cmds(configData, full_path) 
    except:
        traceback.print_exc()
        pass  
    
def install_mdex(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(endeca_modules+'.mdex_helper')
        mymod.install_mdex(configData, full_path)        
    except:
        traceback.print_exc()
        pass  

def install_platformServices(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(endeca_modules+'.platform_helper')
        mymod.install_platformServices(configData, full_path)        
    except:
        traceback.print_exc()
        pass  
    
def install_toolsAndFramework(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(endeca_modules+'.tools_helper')
        mymod.install_toolsAndFramework(configData, full_path)        
    except:
        traceback.print_exc()
        pass  
    
def install_cas(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(endeca_modules+'.cas_helper')
        mymod.install_cas(configData, full_path)        
    except:
        traceback.print_exc()
        pass              

def install_oracle_db(configData, full_path):
    try:
        _set_product_versions(configData)
        mymod = importlib.import_module(db_modules+'.oracle_rdbms_install')
        mymod.install_oracle(configData, full_path)        
    except:
        traceback.print_exc()
        pass     