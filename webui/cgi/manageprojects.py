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

import cgi, cgitb, json
import sys
import traceback
from oc_provision_config import orchestration_helper_webui as orchestration_helper
from oc_provision_config import instance_type_config_webui as instance_type_config

def load_project_data(project_name):
    """
    Load project data from properties file
    """    
    
    global identity_domain
    global username
    global image_name    
    global os_project_name
    global os_image_name      
    data_type = "project"
    
    identity_domain = orchestration_helper.get_config_item(project_name, project_name, 'identity_domain', data_type)
    username = orchestration_helper.get_config_item(project_name, project_name, 'username', data_type)
    image_name = orchestration_helper.get_config_item(project_name, project_name, 'image_name', data_type)
    os_project_name = orchestration_helper.get_config_item(project_name, project_name, 'openstack_project', data_type)
    os_image_name = orchestration_helper.get_config_item(project_name, project_name, 'openstack_image_name', data_type)    
    
    projdata = {'opc': {'Domain': identity_domain, 'username': username, 'image': image_name}, 'openstack': {'os_project_name': os_project_name, 'os_image_name': os_image_name}}
    return (json.JSONEncoder().encode(projdata))   

project_data = {}

form = cgi.FieldStorage() 

# Get data from fields
action = form.getvalue('action')
project_name = form.getvalue('project_name')

print "Content-type: application/json"
print 

"""
************************************
Logic for projects
************************************
"""    
if (action == "list_projects"):
    project_dirs = orchestration_helper.get_existing_projects()
    if project_dirs:
        for idx, proj in enumerate(project_dirs):
            project_data[idx] = proj

    print(json.JSONEncoder().encode(project_data))

if (action == "select_project"):
    selected_project = form.getvalue('selected_project')
    projectdata = load_project_data(selected_project)

    print(json.JSONEncoder().encode(projectdata))   
    
if (action == "add_project_form"):
    selected_project = form.getvalue('selected_project')
    projdata = {'new_project_name': '', 'opc_identity_domain': '', 'opc_username': '', 'opc_image_name': '', 'openstack_project_name': '', 'openstack_image_name': ''}
    enc = json.JSONEncoder(sort_keys=True)
    print(enc.encode(projdata))       

if (action == "edit_project_form"):
    selected_project = form.getvalue('selected_project')
    projectdata = load_project_data(selected_project)
    jsonData = json.loads(projectdata)
    opc_proj_data = jsonData['opc']
    os_proj_data = jsonData['openstack']
    projdatafields = {'opc_identity_domain': opc_proj_data['Domain'], 'opc_username': opc_proj_data['username'], 'opc_image_name': opc_proj_data['image'], 
                      'openstack_project_name': os_proj_data['os_project_name'], 'openstack_image_name': os_proj_data['os_image_name']}
    enc = json.JSONEncoder(sort_keys=True)
    print(enc.encode(projdatafields))    

if (action == "add_project"):
    new_project_name = form.getvalue('new_project_name')
    opc_identity_domain = form.getvalue('opc_identity_domain')
    opc_username = form.getvalue('opc_username')
    opc_image_name = form.getvalue('opc_image_name')
    openstack_project_name = form.getvalue('openstack_project_name')
    openstack_image_name = form.getvalue('openstack_image_name')
    
    data_type = "project"
    
    domain_data = {}
    domain_data['identity_domain'] = opc_identity_domain 
    domain_data['username'] = opc_username
    domain_data['image_name'] = opc_image_name
    domain_data['openstack_project'] = openstack_project_name
    domain_data['openstack_image_name'] = openstack_image_name
    
    compute_name = None
    try:
        if (opc_identity_domain != None) and (opc_username != None):
            compute_name = "/Compute-" + opc_identity_domain + "/" + opc_username + "/"
        domain_data['compute_name'] = compute_name 
        orchestration_helper.make_project(new_project_name)
        orchestration_helper.add_config_section(new_project_name, data_type, new_project_name, domain_data)
        response_data = {'project': new_project_name, 'status': 'success', 'message': 'Project ' + new_project_name + ' Added'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        response_data = {'project': new_project_name, 'status': 'error', 'message': 'Adding Project Failed ', 'errormsg': value.strerror}
                  
    print(json.JSONEncoder().encode(response_data))   
    
if (action == "update_project"):
    
    new_project_name = form.getvalue('new_project_name')
    opc_identity_domain = form.getvalue('opc_identity_domain')
    opc_username = form.getvalue('opc_username')
    opc_image_name = form.getvalue('opc_image_name')
    openstack_project_name = form.getvalue('openstack_project_name')
    openstack_image_name = form.getvalue('openstack_image_name')
    
    data_type = "project"
    
    domain_data = {}
    domain_data['identity_domain'] = opc_identity_domain 
    domain_data['username'] = opc_username
    domain_data['image_name'] = opc_image_name
    domain_data['openstack_project'] = openstack_project_name
    domain_data['openstack_image_name'] = openstack_image_name
    
    compute_name = None
    try:
        if (opc_identity_domain != None) and (opc_username != None):
            compute_name = "/Compute-" + opc_identity_domain + "/" + opc_username + "/"
        domain_data['compute_name'] = compute_name
        for key, value in domain_data.iteritems():
            orchestration_helper.update_config_section(new_project_name, data_type, new_project_name, key, str(value))
        response_data = {'project': new_project_name, 'status': 'success', 'message': 'Project ' + new_project_name + ' Updated'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        response_data = {'project': new_project_name, 'status': 'error', 'message': 'Updating Project Failed ', 'errormsg': value}
                  
    print(json.JSONEncoder().encode(response_data))      

if (action == "delete_project"):
    
    selected_project = ""
    
    try:
        selected_project = str(form.getvalue('selected_project'))
        orchestration_helper.delete_project(selected_project)
        response_data = {'project': selected_project, 'status': 'success', 'message': 'Project Deleted'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        response_data = {'project': selected_project, 'status': 'error', 'message': 'Delete Failed ', 'errormsg': value.strerror}
        
    print(json.JSONEncoder().encode(response_data))


"""
************************************
Logic for storage
************************************
"""      
if (action == "list_storage"):

    data_type = "storage"
    selected_project = form.getvalue('selected_project')
    storage_data = {}
    if selected_project:
        storage_sections = orchestration_helper.get_section_data(selected_project, data_type)
        if storage_sections:
            for idx, section in enumerate(storage_sections):
                storage_data[idx] = section
        
    print(json.JSONEncoder().encode(storage_data))  

if (action == "add_storage_form"):
    selected_project = form.getvalue('selected_project')
    projdata = {'name': '', 'radio': {'/oracle/public/storage/default': '', '/oracle/public/storage/latency' : ''} , 'description': '', 'size': ''}
    enc = json.JSONEncoder(sort_keys=True)
    print(enc.encode(projdata))       

if (action == "add_storage"):
    name = form.getvalue('name')
    properties = form.getvalue('properties')
    description = form.getvalue('description')
    size = form.getvalue('size')
    selected_project = str(form.getvalue('selected_project'))
    
    # append g for GB
    size += 'g';
    
    data_type = "storage"
    
    storage_data = {}
    storage_data['name'] = name 
    storage_data['properties'] = properties
    storage_data['description'] = description
    storage_data['size'] = size
    
    try:
        orchestration_helper.add_config_section(selected_project, data_type, name, storage_data)
        response_data = {'storage': name, 'status': 'success', 'message': 'Storage ' + name + ' Added'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        response_data = {'storage': name, 'status': 'error', 'message': 'Adding Storage Failed ', 'errormsg': value.strerror}
                  
    print(json.JSONEncoder().encode(response_data))   

if (action == "update_storage"):
    
    storage_name = form.getvalue('name')
    properties = form.getvalue('properties')
    description = form.getvalue('description')
    size = form.getvalue('size')
    selected_project = str(form.getvalue('selected_project'))
    
    data_type = "storage"
    
    storage_data = {}
    storage_data['properties'] = properties
    storage_data['description'] = description
    storage_data['size'] = size
    
    try:
        for key, value in storage_data.iteritems():
            orchestration_helper.update_config_section(selected_project, data_type, storage_name, key, str(value))
        response_data = {'storage': storage_name, 'status': 'success', 'message': 'Storage ' + storage_name + ' Updated'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        response_data = {'storage': new_project_name, 'status': 'error', 'message': 'Updating Storage Failed ', 'errormsg': value}
                  
    print(json.JSONEncoder().encode(response_data))    
    
if (action == "edit_storage_form"):
    selected_project = form.getvalue('selected_project')
    selected_storage = str(form.getvalue('selected_storage'))
    data_type = "storage"
    
    storagelistdata = orchestration_helper.get_config_items(selected_project, data_type, selected_storage)
    
    # convert to dict to make life easier
    storagedatafields = {}
    for idx , (key, value) in enumerate(storagelistdata):
        storagedatafields[key] = value
    
    storagedataresponse = {'name': storagedatafields['name'], 'description': storagedatafields['description'], 'properties': storagedatafields['properties'], 
                           'size': storagedatafields['size']}
    enc = json.JSONEncoder(sort_keys=True)
    print(enc.encode(storagedataresponse))  
            
if (action == "delete_storage"):
    
    data_type = "storage"        
    try:
        selected_project = str(form.getvalue('selected_project'))
        selected_storage = str(form.getvalue('selected_storage'))
        orchestration_helper.delete_config_section(selected_project, data_type, selected_storage)
        response_data = {'storage': selected_storage, 'status': 'success', 'message': 'Storage Deleted'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        response_data = {'storage': selected_storage, 'status': 'error', 'message': 'Delete Failed ', 'errormsg': value.strerror}
        
    print(json.JSONEncoder().encode(response_data))   
    
"""
************************************
Logic for instances
************************************
"""        
if (action == "list_instances"):

    data_type = "instances"
    selected_project = form.getvalue('selected_project')
    instance_data = {}
    if selected_project:
        instance_sections = orchestration_helper.get_section_data(selected_project, data_type)
        if instance_sections:
            for idx, section in enumerate(instance_sections):
                instance_data[idx] = section
        
    print(json.JSONEncoder().encode(instance_data)) 
    
if (action == "delete_instance"):
    
    data_type = "instances"        
    try:
        selected_project = str(form.getvalue('selected_project'))
        selected_instance = str(form.getvalue('selected_instance'))
        orchestration_helper.delete_config_section(selected_project, data_type, selected_instance)
        response_data = {'instance': selected_instance, 'status': 'success', 'message': 'Instance Deleted'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        response_data = {'instance': selected_instance, 'status': 'error', 'message': 'Delete Failed ', 'errormsg': value.strerror}
        
    print(json.JSONEncoder().encode(response_data))       


# return data for the add instance form, showing types to select from
if (action == "add_instance_form"):
    
    instance_types = {'ATG Install': 'atg', 'WebLogic - Admin Server': 'weblogic', 'WebLogic - Managed Server': 'weblogicManagedServer', 
                      'Endeca - all components': 'endeca', 'Endeca - DGraph only': 'dgraph', 'OTD install only': 'otd', 
                      'OTD configuration': 'otdconfig', 'Oracle Database': 'db'}
        
    enc = json.JSONEncoder(sort_keys=True)
    print(enc.encode(instance_types))   

# add a new instance    
if (action == "add_instance"):
    
    data_type = "instances"
    
    instance_name = form.getvalue('instance_name')
    hostname = form.getvalue('hostname', default='')
    sshkey_name = form.getvalue('sshkey_name', default='')
    opc_shape = form.getvalue('opc_shape', default='')
    openstack_flavor = form.getvalue('openstack_flavor', default='')
    target_platform = form.getvalue('target_platform', default='')
    instance_types = form.getvalue('instance_types')
    config_source = form.getvalue('config_source', default='')
    attached_storage = form.getvalue('attached_storage', default='')
    json_blob = form.getvalue('json_blob')
    selected_project = str(form.getvalue('selected_project'))
    
    optional_data_types = []
    if ('copy_ssh_keys' in json_blob):
        optional_data_types.append('copy_ssh_keys')
    if ('advanced_storage' in json_blob):
        optional_data_types.append('advanced_storage')
    if ('WEBLOGIC_datasources' in json_blob):
        optional_data_types.append('weblogicDatasources')
    if ('ATGPATCH_install' in json_blob):
        optional_data_types.append('atgpatch')                        
    
    instance_data = {}
    instance_data['targetPlatform'] = target_platform
    instance_data['configSource'] = config_source
    instance_data['instanceTypes'] = instance_types    
    instance_data['name'] = instance_name
    instance_data['hostname'] = hostname
    instance_data['opc_shape'] = opc_shape
    instance_data['openstack_flavor'] = openstack_flavor
    instance_data['sshkeyName'] = sshkey_name
    instance_data['jsonData'] = json_blob
    instance_data['attachedStorage'] = attached_storage
    instance_data['optional_data_types'] = ",".join(optional_data_types)

    try:
        orchestration_helper.add_config_section(selected_project, data_type, instance_name, instance_data)    
        response_data = {'instance': instance_name, 'status': 'success', 'message': 'Instance Added'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        response_data = {'instance': instance_name, 'status': 'error', 'message': 'Add Instance Failed ', 'errormsg': str(value)}    
    
    
    print(json.JSONEncoder().encode(response_data))     
        
# get the required fields for the type of instance selected
if (action == "set_instance_type"):
    instance_types = form.getvalue('instancetypes[]')
    target_platform = form.getvalue('targetplatform')
    config_source = form.getvalue('configsource')
    
    instance_fields = ["instance_name", "hostname", "sshkey_name"]
    
    if (target_platform == 'opc'):
        instance_fields.append("opc_shape")
    elif (target_platform == 'openstack'):
        instance_fields.append("openstack_flavor")
        
    # if only a single type was selected, convert to a list
    if not isinstance(instance_types, list):
        instance_types = instance_types.split()
        
    instance_data_fields = instance_type_config.instance_type_config_web(instance_types)       
    instance_required_data = {}
    instance_optional_data = {}
    # seperate required from optional data blocks
    for datafield in instance_data_fields:
        datafield_json =  instance_data_fields[datafield]
        if 'required' in datafield_json:
            instance_required_data[datafield] = datafield_json
        else:
            instance_optional_data[datafield] = datafield_json
        
                
    response_data = {'instance_types': instance_types, 'target_platform': target_platform, 'config_source': config_source, 'instance_fields': instance_fields, 
                     'required_fields': instance_required_data, 'optional_fields': instance_optional_data}

    enc = json.JSONEncoder(sort_keys=True)                  
    print(enc.encode(response_data))       
    

"""
************************************
Logic for configs
************************************
"""      
if (action == "generate_configs"):
    
    data_type = "instances"        
    try:
        selected_project = str(form.getvalue('selected_project'))
        project_data = json.loads(load_project_data(selected_project))
        orchestration_helper.generate_orchestrations(selected_project, project_data['opc']['Domain'], project_data['opc']['username'], project_data['opc']['image'])
        response_data = {'configs': selected_project, 'status': 'success', 'message': 'Configs generated'}
    except Exception as e:
        type, value, traceback = sys.exc_info()
        print value
        response_data = {'instance': selected_project, 'status': 'error', 'message': 'Generate Configs Failed ', 'errormsg': value.strerror}
        
    print(json.JSONEncoder().encode(response_data))    
