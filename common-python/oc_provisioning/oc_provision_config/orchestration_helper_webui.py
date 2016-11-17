# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (A-Team Cloud Solution Architects)"
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
__module__ = "orchestration_helper_webui"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import ConfigParser 
from collections import defaultdict
import copy 
import errno
import os
import posixpath
import re
import shutil
import yaml
import simplejson as json

identity_domain = ""
username = ""
compute_domain = ""
compute_name = ""
 
# default seclist all servers get added to
default_seclist = "/default/default"

yaml_map = defaultdict(list)

# root for orchestration files
root_orch_dir = "orchestrations"

# property key for instance types
INSTANCE_TYPES_KEY = "instancetypes"

# property key for optional data types
OPTIONAL_DATA_KEY = "optional_data_types"

# property key for instance types
HOSTNAME_KEY = "hostname"

config_file_map = {'storage': 'storage.properties', 'instances': 'instances.properties', 'project': 'project.properties'}
project_directory = "projects"

wrapper_script = "/opt/oracle/install/11.1/pywrapper.sh"

# map the instance types in our property files to the flags we need to pass to our wrapper script. This tells wrapper what to install
# remove weblogicSettings from weblogic map until added to gui
instance_flags = {'atg': ['--java', '--atg'],
                  'weblogic': ['--java', '--weblogic', '--weblogicDomain'],
                  'weblogicManagedServer': ['--java', '--weblogic', '--weblogicManagedServer'],
                  'otd': ['--java', '--otdInstall'],
                  'otdconfig': ['--otdConfig'],
                  'endeca': ['--endeca'],
                  'dgraph': ['--dgraph'],
                  'db': ['--db']}

# common/optional flags that can be used based on what data is in the json
optional_flags = {'copy_ssh_keys': ['--copy_ssh_keys'],
                  'advanced_storage': ['--advanced_storage'],
                  'weblogicDatasources': ['--weblogicDatasources'],
                  'atgpatch': ['--atgpatch']}

# map the instance type to the security lists the instance needs to be a part of
seclist_map = {'atg': ['atg_instances'],
               'weblogic' : ['weblogic_admin', 'atg_support'],
               'weblogicManagedServer' : ['atg_instances'],
               'otd' : ['otd_server'],
               'endeca' : ['endeca_instances'],
               'dgraph' : ['endeca_instances'],
               'db' : ['db_server']}

def get_existing_projects():
    return os.listdir(project_directory)

def make_project(project_name):
    dir_to_make = posixpath.join(project_directory, project_name)
    os.mkdir(dir_to_make)
    
def delete_project(project_name):
    dir_to_del = posixpath.join(project_directory, project_name)
    shutil.rmtree(dir_to_del) 

def generate_orchestrations(project_name, domain, user, image_name):
    """
    main function to generate orchs and yaml
    """          
    global identity_domain
    global username
    global compute_domain
    global compute_name
    
    identity_domain = domain
    username = user

    compute_domain = "/Compute-" + identity_domain
    compute_name = compute_domain + "/" + username    
    
    # delete any exinsting orchs    
    remove_existing_orchestrations(project_name)
    
    generate_secapp_data(project_name)
    generate_seclist_data(project_name)
    generate_storage_data(project_name)
    generate_instance_data(project_name, image_name)
    create_common_opc_ansible_configs(project_name)
    generate_storage_yaml(project_name)
    generate_instance_yaml(project_name)
    create_shell_wrapper(project_name)
    
    
def remove_existing_orchestrations(project_name):
    orch_dir = project_directory + "/" + project_name + "/" + root_orch_dir
    if os.path.exists(orch_dir):
        try:
            shutil.rmtree(orch_dir)            
        except:
            print "cannot remove existing orchestration tree"  
         
def generate_storage_yaml(project_name):
    """
    Generate ansible playbooks for OPC storage
    """          
    data_type = "storage"
    sections = get_section_data(project_name, data_type)
    for section in sections:
        storage_description = get_config_item(project_name, section, 'description', data_type)
        storage_size = get_config_item(project_name, section, 'size', data_type)
        storage_properties = get_config_item(project_name, section, 'properties', data_type)
        create_storage_yaml(section, storage_description, storage_properties, storage_size, project_name)

def generate_instance_yaml(project_name):
    """
    Generate ansible playbooks for OPC or OpenStack instances
    """            
    data_type = "instances"
    sections = get_section_data(project_name, data_type)
    for section in sections:
        target_platform = get_config_item(project_name, section, 'targetPlatform', data_type)
        if (target_platform == 'opc'):
            create_instance_yaml(section, project_name)
        elif (target_platform == 'openstack'):
            create_os_instance_yaml(section, project_name)
               
def create_common_opc_ansible_configs(project_name):
    """
    Base ansible configs
    """            
    # copy ansible default configs
    template_dir = "ansible_templates/"
    ansible_hosts = "ansible_hosts"
    ansible_cfg = "ansible.cfg"
    shared_oc_vars = "opc/oraclecompute_vars.yaml"
    source_library = template_dir + 'library'
    ansible_dir = project_directory + "/" + project_name + "/" + root_orch_dir + "/" + "/ansible"
    
    dst_hosts = ansible_dir + "/" + ansible_hosts
    dst_cfg = ansible_dir + "/" + ansible_cfg
    
    playbook_dir = ansible_dir + "/playbooks"
    dst_shared_vars = playbook_dir + "/" + shared_oc_vars
    
    library_dir = playbook_dir + "/library"
    
    log_dir = ansible_dir + "/logs"
    
    

    if not os.path.exists(ansible_dir):
        try:
            os.makedirs(ansible_dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise   

    if not os.path.exists(playbook_dir):
        try:
            os.makedirs(playbook_dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise  
            
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise                
                            
    if not os.path.isfile(dst_hosts):
        shutil.copy(template_dir + ansible_hosts, dst_hosts)
        
    if not os.path.isfile(dst_cfg):
        shutil.copy(template_dir + ansible_cfg, dst_cfg)
        
    if not os.path.isfile(dst_shared_vars):
        shutil.copy(template_dir + shared_oc_vars, playbook_dir)

    if not os.path.exists(library_dir):
        shutil.copytree(source_library, library_dir)

def create_storage_yaml(section_name, storage_description, storage_properties, storage_size, project_name):
    """
    Create yaml from template for OPC storage
    """            
    data_type = "storage"
    
    vars_dict = {'sectionname' : section_name, 'storagevolume' : '{{ sectionname }}', 'storagevolumesize': storage_size, 'storagevolumedescription': storage_description, 'storagevolumeprops': storage_properties}
    
    storage_name = section_name + "_storage"
    storage_yaml = storage_name + ".yaml"
    storage_yaml_vars = storage_name + "_vars.yaml"
    storage_cleanup_yaml = storage_name + "_cleanup.yaml"
    vars_files = ['../oraclecompute_vars.yaml', storage_yaml_vars]
    
    # create vars file
    write_yaml_data(vars_dict, storage_yaml_vars, data_type, project_name)
    
    # read the storage create template, and update the name and vars files
    create_template = file('ansible_templates/opc/storage.yaml', 'r')
    create_data = yaml.load(create_template) 
    create_data[0]['name'] = "Create " + storage_name
    create_data[0]['vars_files'] = vars_files
    write_yaml_data(create_data, storage_yaml, data_type, project_name)
    
    # read the storage delete template, and update the name and vars files
    clean_template = file('ansible_templates/opc/storage_cleanup.yaml', 'r')
    clean_data = yaml.load(clean_template) 
    clean_data[0]['name'] = "Delete " + storage_name
    clean_data[0]['vars_files'] = vars_files
    write_yaml_data(clean_data, storage_cleanup_yaml, data_type, project_name)
    
def create_os_instance_yaml(section_name, project_name):
    """
    Create yaml from template for OpenStack instances
    """   
    data_type = "instances"
            
    instance_name = section_name + "_os_instance"
    instance_yaml = instance_name + ".yaml"
    instance_cleanup_yaml = instance_name + "_cleanup.yaml"

    # read the instance create template
    create_template = file('ansible_templates/openstack/os_instance.yaml', 'r')
    create_data = yaml.load(create_template) 
    create_data[0]['name'] = "Create " + instance_name
    create_data[0]['tasks'][0]['os_server']['name'] = get_config_item(project_name, section_name, HOSTNAME_KEY, data_type)
    create_data[0]['tasks'][0]['os_server']['image'] = get_config_item(project_name, project_name, 'openstack_image_name', 'project')
    create_data[0]['tasks'][0]['os_server']['flavor'] = get_config_item(project_name, section_name, 'openstack_flavor', data_type)
    create_data[0]['tasks'][0]['os_server']['key_name'] = get_config_item(project_name, section_name, 'sshkeyName', data_type)
    
    instance_types = get_config_item(project_name, section_name, INSTANCE_TYPES_KEY, data_type).split(',')
    optional_data_types = get_config_item(project_name, section_name, OPTIONAL_DATA_KEY, data_type)
    config_source = get_config_item(project_name, section_name, 'configSource', data_type)
    
    script_data = {}
    # add script tag that we pick up at instance boot
    script_data['script'] = wrapper_script + " " + compute_script_flags(instance_types, optional_data_types, config_source)
    
    # add json data to config products with if configSource is set to user-data
    if (config_source == 'user-data'):
        # need to know we are using openstack if we want user meta-data
        script_data['script'] += ' --openstack'
        script_data['commerceSetup'] = json.loads(get_config_item(project_name, section_name, 'jsondata', data_type))    
    create_data[0]['tasks'][0]['os_server']['userdata'] = json.dumps(script_data)
    
    write_yaml_data(create_data, instance_yaml, data_type, project_name)
    
    # read the instance delete template
    clean_template = file('ansible_templates/openstack/os_instance_cleanup.yaml', 'r')
    clean_data = yaml.load(clean_template) 
    clean_data[0]['name'] = "Delete " + instance_name
    clean_data[0]['tasks'][0]['os_server']['name'] = get_config_item(project_name, section_name, HOSTNAME_KEY, data_type)
    write_yaml_data(clean_data, instance_cleanup_yaml, data_type, project_name)       
    
def create_instance_yaml(section_name, project_name):
    """
    Create yaml from template for OPC instances
    """               
    data_type = "instances"
        
    vars_dict = {'environmentname' : section_name, 'envorchestration' : '{{ environmentname }}'}
    
    instance_name = section_name + "_instance"
    instance_yaml = instance_name + ".yaml"
    instance_yaml_vars = instance_name + "_vars.yaml"
    instance_cleanup_yaml = instance_name + "_cleanup.yaml"
    vars_files = ['../oraclecompute_vars.yaml', instance_yaml_vars]
    
    # create vars file
    write_yaml_data(vars_dict, instance_yaml_vars, data_type, project_name)
    
    # add json template name to create instance with
    orch_json = "{{ lookup('template', '../templates/" + section_name + ".json', convert_data=False) }}"
    
    # read the instance create template, and update the name and vars files
    create_template = file('ansible_templates/opc/instance.yaml', 'r')
    create_data = yaml.load(create_template) 
    create_data[0]['name'] = "Create " + instance_name
    create_data[0]['vars_files'] = vars_files
    tasks = create_data[0]['tasks']
    for task in tasks:
        if task['name'] == 'add orchestration':            
            task['oc_orchestration']['orchestration'] = orch_json
    write_yaml_data(create_data, instance_yaml, data_type, project_name)
    
    # read the instance delete template, and update the name and vars files
    clean_template = file('ansible_templates/opc/instance_cleanup.yaml', 'r')
    clean_data = yaml.load(clean_template) 
    clean_data[0]['name'] = "Delete " + instance_name
    clean_data[0]['vars_files'] = vars_files
    write_yaml_data(clean_data, instance_cleanup_yaml, data_type, project_name)
                                 
def get_section_data(project_name, data_type):
    config = ConfigParser.ConfigParser()
    storage_data = project_directory + "/" + project_name + "/" + config_file_map[data_type]
    config.read(storage_data)
    return config.sections()

def does_name_exist(project_name, data_type, section_name):
    config = ConfigParser.ConfigParser()
    storage_data = project_directory + "/" + project_name + "/" + config_file_map[data_type]
    config.read(storage_data)
    return config.has_section(section_name)

def get_all_attached_storage(project_name, data_type):
    attached_storage = []
    
    config = ConfigParser.ConfigParser()
    storage_data = project_directory + "/" + project_name + "/" + config_file_map[data_type]
    config.read(storage_data) 
        
    for section in config.sections():
        if config.has_option(section, 'attachedStorage'):
            attached_storage.append(config.get(section, 'attachedStorage'))
    return attached_storage
        
        
def get_config_items(project_name, data_type, section_name):
    config = ConfigParser.ConfigParser()
    storage_data = project_directory + "/" + project_name + "/" + config_file_map[data_type]
    config.read(storage_data)
    return config.items(section_name)

def get_config_item(project_name, section, option, data_type):
    if not project_name:
        return None
    config = ConfigParser.ConfigParser()
    storage_data = project_directory + "/" + project_name + "/" + config_file_map[data_type]
    config.read(storage_data)
    try:
        items = config.get(section, option)
    except ConfigParser.NoSectionError:
        return []
    return items

def update_config_section(project_name, data_type, section_name, prop_name, prop_value):
    config = ConfigParser.ConfigParser()
    storage_data = project_directory + "/" + project_name + "/" + config_file_map[data_type]
    config.read(storage_data)
    # print "updating " + section_name + prop_name + prop_value
    config.set(section_name, prop_name, prop_value)
    with open(storage_data, 'wb') as configfile:
        config.write(configfile)
    # print ">> " + prop_name + " updated"

def add_config_section(project_name, data_type, section_name, section_data):
    config = ConfigParser.ConfigParser()
    storage_data = project_directory + "/" + project_name + "/" + config_file_map[data_type]
    config.read(storage_data)
    # print "adding " + section_name
    config.add_section(section_name)
    for key in section_data.keys():
        config.set(section_name, key, section_data[key])
        
    with open(storage_data, 'wb') as configfile:
        config.write(configfile)
        
def delete_config_section(project_name, data_type, section_name):
    config = ConfigParser.ConfigParser()
    storage_data = project_directory + "/" + project_name + "/" + config_file_map[data_type]
    config.read(storage_data)
    config.remove_section(section_name)    
    with open(storage_data, 'wb') as configfile:
        config.write(configfile)
        
def generate_storage_data(project_name):
    """
    Create orchs from template for OPC storage
    """                  
    data_type = "storage"
    data_file = 'orch_templates/storage.template'
    with open(data_file) as data_file:    
        data = json.load(data_file)
 
    sections = get_section_data(project_name, data_type)
    
    for section in sections:
        data['description'] = section + " Commerce Storage"
        data['name'] = compute_name + "/" + section
        data['oplans'][0]['objects'][0]['name'] = compute_name + "/" + section
        data['oplans'][0]['objects'][0]['description'] = get_config_item(project_name, section, 'description', data_type)
        data['oplans'][0]['objects'][0]['size'] = get_config_item(project_name, section, 'size', data_type)
        data['oplans'][0]['objects'][0]['properties'][0] = get_config_item(project_name, section, 'properties', data_type)

        write_orch_data(data, section, data_type, project_name)    

def create_seclist_yaml(project_name, allseclist_list):
    """
    Generate seclist yaml
    """  
        
    data_type = "seclist"
    seclist_yaml_file = "seclist.yaml"
    seclist_cleanup_yaml_file = "seclist_cleanup.yaml"
    
    # read the seclist create template
    create_template = file('ansible_templates/opc/seclist.yaml', 'r')
    create_data = yaml.load(create_template)
    
    # read the seclist delete template
    cleanup_template = file('ansible_templates/opc/seclist_cleanup.yaml', 'r')
    cleanup_data = yaml.load(cleanup_template)    
        
    for seclist in allseclist_list:
        # generate create list
        seclist_create = [{'name': 'add seclist', 'ignore_errors' : 'yes', 'oc_security_list': {'action': 'create', 'cookie': '{{ cookie.cookie }}', 'endpoint': '{{ endpoint }}', 'name': '', 'resourcename': ''}}]
        seclist_create[0]['oc_security_list']['name'] = seclist['name']
        seclist_create[0]['oc_security_list']['resourcename'] = seclist['name']
        create_data[0]['tasks'].append(seclist_create[0])
        
        # generate delete list
        seclist_delete = [{'name': 'delete seclist', 'ignore_errors' : 'yes', 'oc_security_list': {'action': 'delete', 'cookie': '{{ cookie.cookie }}', 'endpoint': '{{ endpoint }}', 'name': '', 'resourcename': ''}}]
        seclist_delete[0]['oc_security_list']['name'] = seclist['name']
        seclist_delete[0]['oc_security_list']['resourcename'] = seclist['name']
        cleanup_data[0]['tasks'].append(seclist_delete[0])
        

    write_yaml_data(create_data, seclist_yaml_file, data_type, project_name)
    write_yaml_data(cleanup_data, seclist_cleanup_yaml_file, data_type, project_name)

def create_secapp_yaml(project_name, all_secapps_list):
    """
    Generate secapp yaml
    """  
        
    data_type = "secapp"
    secapp_yaml_file = "secapp.yaml"
    secapp_cleanup_yaml_file = "secapp_cleanup.yaml"
    
    # read the seclist create template
    create_template = file('ansible_templates/opc/secapp.yaml', 'r')
    create_data = yaml.load(create_template)
    
    # read the seclist delete template
    cleanup_template = file('ansible_templates/opc/secapp_cleanup.yaml', 'r')
    cleanup_data = yaml.load(cleanup_template)    
        
    for secapp in all_secapps_list:
        # generate create list
        secapp_create = [{'name': 'add secapp', 'oc_security_application': {'action': 'create', 'cookie': '{{ cookie.cookie }}', 'endpoint': '{{ endpoint }}', 'name': '', 'resourcename': '', 'dport': '', 'protocol': ''}}]
        secapp_create[0]['oc_security_application']['name'] = secapp['name']
        secapp_create[0]['oc_security_application']['resourcename'] = secapp['name']
        secapp_create[0]['oc_security_application']['dport'] = secapp['dport']
        secapp_create[0]['oc_security_application']['protocol'] = secapp['protocol']        
        create_data[0]['tasks'].append(secapp_create[0])
        
        # generate delete list
        secapp_delete = [{'name': 'delete secapp', 'oc_security_application': {'action': 'delete', 'cookie': '{{ cookie.cookie }}', 'endpoint': '{{ endpoint }}', 'name': '', 'resourcename': '', 'dport': '', 'protocol': ''}}]
        secapp_delete[0]['oc_security_application']['name'] = secapp['name']
        secapp_delete[0]['oc_security_application']['resourcename'] = secapp['name']
        secapp_delete[0]['oc_security_application']['dport'] = secapp['dport']
        secapp_delete[0]['oc_security_application']['protocol'] = secapp['protocol']
        cleanup_data[0]['tasks'].append(secapp_delete[0])
        

    write_yaml_data(create_data, secapp_yaml_file, data_type, project_name)
    write_yaml_data(cleanup_data, secapp_cleanup_yaml_file, data_type, project_name)


def generate_seclist_data(project_name):
    """
    Generate security list orchestrations
    """        
    data_type = "seclist"
    data_file = 'orch_templates/seclist.template'
    with open(data_file) as data_file:    
        master_data = json.load(data_file)
        data_file.close()
        
    data = copy.deepcopy(master_data)
    data['name'] = compute_name + "/commerce_seclist_orchestration"
    
    unique_all_seclists = compute_all_seclists(project_name)
    # remove the default seclist. If we try to create or remove default, OPC will not let us and throw an error
    unique_all_seclists.discard(compute_domain + default_seclist)
    allseclist_list = []
    
    for seclist in unique_all_seclists:
        temp_seclist = {}
        temp_seclist['name'] = seclist
        allseclist_list.append(temp_seclist)
    
    data['oplans'][0]['objects'] = allseclist_list
    write_orch_data(data, "seclist", data_type, project_name)
    
    # pass our generated list to be written to yaml for ansible
    create_seclist_yaml(project_name, allseclist_list)


def _has_nested_key(search_data, key):
    """
    Recurse dictionary looking for a specific key
    """        
    if key in search_data: return True
    for k, v in search_data.items():
        if isinstance(v, dict):
            item = _has_nested_key(v, key)
            if item is not None:
                return True
    return None 
    
def generate_secapp_data(project_name):
    """
    Generate security app orchestrations
    """       
    data_type = "secapp"
    data_file_type = "instances"
    data_file = 'orch_templates/secapp.template'
    with open(data_file) as data_file:    
        master_data = json.load(data_file)
        data_file.close()
        
    data = copy.deepcopy(master_data)
    data['name'] = compute_name + "/commerce_secapps_orchestration"
    
    # get all instance sections
    sections = get_section_data(project_name, data_file_type)
    
    json_data = {}
    
    # hold all the ports we want to add to the secapp orch file
    secapp_port_map = {}
    
    for section in sections:
        # get json data for this section
        json_data = json.loads(get_config_item(project_name, section, 'jsondata', data_file_type))

        # add ports that are not part of the JSON config at this point
        if (_has_nested_key(json_data, 'OTD_install')):
            secapp_port_map['otd_adminPort'] = "8989"
        if (_has_nested_key(json_data, 'toolsAndFramework')):
            secapp_port_map['endeca_workbenchPort'] = "8006"
        if (_has_nested_key(json_data, 'platformServices')):
            secapp_port_map['endeca_dgraphPort'] = "15000"
        if (_has_nested_key(json_data, 'WEBLOGIC_managed_server')):
            secapp_port_map['wls_nodemanPort'] = "5556"
        if (_has_nested_key(json_data, 'ORACLE_RDBMS_install')):
            secapp_port_map['sqlnetPort'] = "1521"
            secapp_port_map['oracle_emPort'] = "1158"
                             
        # check if specific JSON sections exist. If they do, add ports we need from those sections
        if (_has_nested_key(json_data, 'WEBLOGIC_common')):
            secapp_port_map['wl_adminHttpPort'] = json_data['WEBLOGIC_common']['wl_adminHttpPort']
            secapp_port_map['wl_adminHttpsPort'] = json_data['WEBLOGIC_common']['wl_adminHttpsPort']
            
        if (_has_nested_key(json_data, 'WEBLOGIC_managed_servers')):
            managed_servers = []
            managed_servers = json_data['WEBLOGIC_managed_servers']
            for managed_server in managed_servers:                
                if 'atgRmiPort' in managed_server:
                    secapp_port_map['atg_rmi_' + managed_server['atgRmiPort']] = managed_server['atgRmiPort']
                if 'atgFdPort' in managed_server:
                    secapp_port_map['atg_fd_' + managed_server['atgFdPort']] = managed_server['atgFdPort']                    
                if 'atgDrpPort' in managed_server:
                    secapp_port_map['atg_drp_' + managed_server['atgDrpPort']] = managed_server['atgDrpPort']                    
                if 'bccFileSyncPort' in managed_server:
                    secapp_port_map['atg_bccsync_' + managed_server['bccFileSyncPort']] = managed_server['bccFileSyncPort']                    
                if 'atgLockManPort' in managed_server:
                    secapp_port_map['atg_lock_' + managed_server['atgLockManPort']] = managed_server['atgLockManPort']   
        
        if (_has_nested_key(json_data, 'OTD_config')):           
            otd_servers = []
            otd_servers = json_data['OTD_config']
            for otd_server in otd_servers:                
                if 'virtualServerPort' in otd_server:
                    secapp_port_map['otd_lb_' + otd_server['configName']] = otd_server['virtualServerPort']                                                      

    all_secapps_list = []
    for key, value in secapp_port_map.iteritems():
        temp_secapp = {}
        temp_secapp['name'] = compute_name + "/" + key
        temp_secapp['dport'] = int(value)
        temp_secapp['protocol'] = 'tcp'
        all_secapps_list.append(temp_secapp)

    
    data['oplans'][0]['objects'] = all_secapps_list
    write_orch_data(data, data_type, data_type, project_name)
    
    create_secapp_yaml(project_name, all_secapps_list)       
                           
def generate_instance_data(project_name, image_name):
    """
    Generate instance orchestrations
    """        
    data_type = "instances"
    data_file = 'orch_templates/instance.template'
    with open(data_file) as data_file:    
        master_data = json.load(data_file)
        data_file.close()
        
    data = copy.deepcopy(master_data)
    
    sections = get_section_data(project_name, data_type)
    
    for section in sections:
        json_data = {}
        
        data = copy.deepcopy(master_data)
       
        data['description'] = section + " Commerce Instance"
        data['name'] = compute_name + "/" + section
        data['oplans'][0]['objects'][0]['instances'][0]['label'] = section
        data['oplans'][0]['objects'][0]['instances'][0]['name'] = compute_name + "/" + section
        hostname = get_config_item(project_name, section, HOSTNAME_KEY, data_type)
        data['oplans'][0]['objects'][0]['instances'][0]['hostname'] = hostname
        data['oplans'][0]['objects'][0]['instances'][0]['imagelist'] = compute_name + "/" + image_name
        data['oplans'][0]['objects'][0]['instances'][0]['shape'] = get_config_item(project_name, section, 'opc_shape', data_type)
        data['oplans'][0]['objects'][0]['instances'][0]['sshkeys'][0] = compute_name + "/" + get_config_item(project_name, section, 'sshkeyname', data_type)
        
        instance_types = get_config_item(project_name, section, INSTANCE_TYPES_KEY, data_type).split(',')
        optional_data_types = get_config_item(project_name, section, OPTIONAL_DATA_KEY, data_type)
        config_source = get_config_item(project_name, section, 'configSource', data_type)
        
        # add json data to config products with if configSource is set to user-data
        if (config_source == 'user-data'):
            data['oplans'][0]['objects'][0]['instances'][0]['attributes']['userdata']['commerceSetup'] = json.loads(get_config_item(project_name, section, 'jsondata', data_type))           
        
        data['oplans'][0]['objects'][0]['instances'][0]['attributes']['userdata']['pre-bootstrap']['script'] = wrapper_script + " " + compute_script_flags(instance_types, optional_data_types, config_source)
            
        data['oplans'][0]['objects'][0]['instances'][0]['networking']['eth0']['seclists'] = compute_seclists(hostname, instance_types)
        
        # write json data for configuring installers
        json_data["commerceSetup"] = json.loads(get_config_item(project_name, section, 'jsondata', data_type))

        write_orch_data(json_data, section, 'json', project_name)        
        
        # if instance config has attached storage, add it to our output data
        storage_list = ''
        storage_attachments = []
        storage_list = get_config_item(project_name, section, 'attachedstorage', data_type)
        if storage_list:
            storage_attachments = storage_list.split(',')           
            if storage_attachments:
                data['oplans'][0]['objects'][0]['instances'][0]['storage_attachments'] = storage_attachments
                for idx, attachment in enumerate(storage_attachments):
                    attachment = compute_name + "/" + attachment
                    tempdict = {'index' : idx + 1, 'volume' : attachment}
                    data['oplans'][0]['objects'][0]['instances'][0]['storage_attachments'][idx] = tempdict
            

        # write orchestration files for direct user use
        write_orch_data(data, section, data_type, project_name)
        # write orchestration files for ansible template use
        write_ansible_orch_template(data, section, data_type, project_name)

def write_ansible_orch_template(data, name, orch_type, project_name):
    
    filename = name + ".json"
    orch_file = project_directory + "/" + project_name + "/" + root_orch_dir + "/ansible/playbooks/templates/" + filename
    
    if not os.path.exists(os.path.dirname(orch_file)):
        try:
            os.makedirs(os.path.dirname(orch_file))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise    
    
    target = open(orch_file, 'w')
    target.write(json.dumps(data))
    target.close()
    
def write_orch_data(data, name, orch_type, project_name):
    
    filename = name + ".json"
    orch_file = project_directory + "/" + project_name + "/" + root_orch_dir + "/" + orch_type + "/" + filename
    
    if not os.path.exists(os.path.dirname(orch_file)):
        try:
            os.makedirs(os.path.dirname(orch_file))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise    
            
    target = open(orch_file, 'w')
    target.write(json.dumps(data, ensure_ascii=True))
    target.close()

def create_shell_wrapper(project_name):
    """
    Create wrapper shell scripts to execute all playbooks in the correct order
    """    
    
    create_shell_cmds = []
    delete_shell_cmds = []
    base_cmd = "ansible-playbook "
    create_wrapper = project_directory + "/" + project_name + "/" + root_orch_dir + "/ansible/opc_wrapper.sh"
    delete_wrapper = project_directory + "/" + project_name + "/" + root_orch_dir + "/ansible/opc_cleanup_wrapper.sh"  
    log_dir = "logs/"   
    
    # the order here matters. Generate in the order you want things created in OPC (secapp, then seclist, then storage, then instance)
    if("seclist" in yaml_map):
        seclist_yaml = yaml_map['seclist']
        for listitem in seclist_yaml:
            junk_path, log_filename = os.path.split(listitem)
            log_filename = re.sub('.yaml', '', log_filename)
            if (('_cleanup.yaml' not in listitem) and ('_vars.yaml' not in listitem)):
                create_shell_cmds.append(base_cmd + listitem + " > " + log_dir + log_filename + ".log " + " 2>&1")
            elif ('_cleanup.yaml' in listitem):
                delete_shell_cmds.insert(0, base_cmd + listitem + " > " + log_dir + log_filename + ".log " + " 2>&1")
                
    if("secapp" in yaml_map):
        secapp_yaml = yaml_map['secapp']
        for listitem in secapp_yaml:
            junk_path, log_filename = os.path.split(listitem)
            log_filename = re.sub('.yaml', '', log_filename)            
            if (('_cleanup.yaml' not in listitem) and ('_vars.yaml' not in listitem)):
                create_shell_cmds.append(base_cmd + listitem + " > " + log_dir + log_filename + ".log " + " 2>&1")
            elif ('_cleanup.yaml' in listitem):                    
                delete_shell_cmds.insert(0, base_cmd + listitem + " > " + log_dir + log_filename + ".log " + " 2>&1")
                
                      
    if("storage" in yaml_map):
        storage_yaml = yaml_map['storage']
        for listitem in storage_yaml:
            junk_path, log_filename = os.path.split(listitem)
            log_filename = re.sub('.yaml', '', log_filename)            
            if (('_cleanup.yaml' not in listitem) and ('_vars.yaml' not in listitem)):
                create_shell_cmds.append(base_cmd + listitem + " > " + log_dir + log_filename + ".log " + " 2>&1")
            elif ('_cleanup.yaml' in listitem):                    
                delete_shell_cmds.insert(0, base_cmd + listitem + " > " + log_dir + log_filename + ".log " + " 2>&1")                
                 
    if("instances" in yaml_map):
        instance_yaml = yaml_map['instances']
        for listitem in instance_yaml:
            junk_path, log_filename = os.path.split(listitem)
            log_filename = re.sub('.yaml', '', log_filename)            
            if (('_cleanup.yaml' not in listitem) and ('_vars.yaml' not in listitem)):
                create_shell_cmds.append(base_cmd + listitem + " > " + log_dir + log_filename + ".log " + " 2>&1 &")
            elif ('_cleanup.yaml' in listitem):
                delete_shell_cmds.insert(0, base_cmd + listitem + " > " + log_dir + log_filename + ".log " + " 2>&1")                   

    create_script = open(create_wrapper, 'w')        
    
    for cmd in create_shell_cmds:
        create_script.write(cmd)
        create_script.write("\n")
    create_script.close()
    
    delete_script = open(delete_wrapper, 'w')        
    
    for cmd in delete_shell_cmds:
        delete_script.write(cmd)
        delete_script.write("\n")
    delete_script.close()
    
    os.chmod(create_wrapper, 0755)
    os.chmod(delete_wrapper, 0755)
    
def write_yaml_data(data, name, yaml_type, project_name):
    
    global yaml_map

    filename = name
    yaml_file = project_directory + "/" + project_name + "/" + root_orch_dir + "/ansible/playbooks/" + yaml_type + "/" + filename
    
    # we want relative path fron ansible for playbook execution
    playbook = "playbooks/" + yaml_type + "/" + filename
    
    # keep running list of all playbooks we generate for the shell wrapper
    yaml_list_item = [playbook]
    yaml_map[yaml_type].extend(yaml_list_item)
    
    if not os.path.exists(os.path.dirname(yaml_file)):
        try:
            os.makedirs(os.path.dirname(yaml_file))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise    
    target = open(yaml_file, 'w')
    target.write(yaml.dump(data, default_flow_style=False, width=1000))
    target.close()

# compute the flags to be passed to the wrapper that kicks everything off
def compute_script_flags(instance_types, optional_data_types, config_source):
    
        all_flags = []
        # use the instance type map
        for instance_type in instance_types:
            for flags in instance_flags[instance_type]:
                all_flags.append(flags)
                
        # use the map for optional flags
        if optional_data_types:
            optional_items = optional_data_types.split(',')
            for optional_type in optional_items:
                for flags in optional_flags[optional_type]:
                    all_flags.append(flags)                
        
        # if there is a configSource defined, add a flag to read it
        if (config_source != ""):
            all_flags.append("--configSource=" + config_source)
            
        # flags can overlap. Use a set to only have unique elements    
        unique_flags = set(all_flags)
        script_params = " ".join(unique_flags)
        
        return script_params
            
def compute_seclists(hostname, instance_types):
        """
        Make a list of all seclists based on hostname, instance type, and our seclist_map. This generates data for a single instance
        """            
        seclists = []
        # add default seclist to all instances
        seclists.append(compute_domain + default_seclist)
        # add this hostname to seclists
        seclists.append(compute_name + "/" + hostname)
        
        seclist_map_values = []
        # add seclists based on seclist_map
        for instance_type in instance_types:
            if instance_type in seclist_map:
                for seclist in seclist_map[instance_type]:
                    seclist_map_values.append(seclist)
                
        unique_seclist_map = set(seclist_map_values)
        for unique_seclist in unique_seclist_map:            
            seclists.append(compute_name + "/" + unique_seclist)

        return seclists             
    
def compute_all_seclists(project_name):
    """
    Make a list of all seclists for instances in project
    """        
    data_type = "instances"
    
    sections = get_section_data(project_name, data_type)
    
    seclists = []
    
    for section in sections:
        instance_types = get_config_item(project_name, section, INSTANCE_TYPES_KEY, data_type).split(',')
        hostname = get_config_item(project_name, section, HOSTNAME_KEY, data_type)
        seclists.extend(compute_seclists(hostname, instance_types))
        
    unique_seclists = set(seclists)

    return unique_seclists      
