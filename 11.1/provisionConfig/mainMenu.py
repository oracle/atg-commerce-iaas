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

import os
import sys

from modules import orchestration_helper, instance_type_config 
import simplejson as json

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (A-Team Cloud Solution Architects)"
__copyright__ = "Copyright (c) 2016  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.0"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

identity_domain = None
username = None
password = None
image_name = None
os_project_name = None
os_image_name = None
project_name = None
compute_name = None

# Main menu
def main_menu():
    os.system('clear')
    local_menu_actions = {
        'main_menu': main_menu,
        '0': select_project,
        '2': manage_storage,
        '3': manage_instances,
        '4': generate_orchestrations,
        'source_menu': main_menu
    }
    local_menu_actions.update(common_menu_actions)
    
    print "Choose an action:"
    
    if (project_name == None):
        print "[0] Select or create a project - [current project is " + str(project_name) + "]"
    else:        
        print "[0] Select or create a project - [current project is " + str(project_name) + "]"
        print "OPC domain details " + "[domain=" + identity_domain + "]" + "[username=" + username + "]" + " [VM image=" + image_name + "]"
        print "OpenStack domain details " + "[project=" + os_project_name + "]" + " [VM image=" + os_image_name + "]"
        print   
        print "[2] Manage storage"
        print "[3] Manage instances"
        print "[4] Generate Orchestration files"
        
        common_menu()
        
    choice = raw_input(" >>  ")
    exec_menu(choice, local_menu_actions)

    return

# Execute menu action
def exec_menu(choice, menu_actions):
    # os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:                        
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            pause()
            menu_actions['source_menu']()
    return

def add_project():
    """
    Add a new project
    """    
    os.system('clear')
    this_function_name = sys._getframe().f_code.co_name
    print "\t[" + this_function_name + "]\n"
    
    global project_name
    
    print "Enter project name:"
    choice = raw_input(" >>  ")
    orchestration_helper.make_project(choice)
    project_name = choice
    domain_info()
    
def select_project():
    """
    Select existing project if they exist
    """    
    os.system('clear')
    this_function_name = sys._getframe().f_code.co_name
    print "\t[" + this_function_name + "]\n"
        
    global project_name
    project_dirs = orchestration_helper.get_existing_projects()
    
    local_menu_actions = {'source_menu': select_project,
                          'a': add_project,
                          'd': "d",
                          'e': 'e'
                         }
    
    local_menu_actions.update(common_menu_actions)
                  
    if project_dirs:
        print "Existing projects:"
        for idx, proj in enumerate(project_dirs):
            print "[" + str(idx) + "] " + proj,
            if proj == project_name:
                print "[selected]"
            else:
                print
            local_menu_actions[str(idx)] = proj
        print ""        

    print "[a]   - Add Project"
    print "[d #] - Delete Project - enter d and the # to delete"
    print "[#]   - Enter number of existing project to select it"

    common_menu()
    choice = raw_input(" >>  ")
    if (choice != 'd') and (choice.isdigit()):
        if (int(choice) <= len(project_dirs) - 1):
            project_name = project_dirs[int(choice)]
            load_project_data()
    elif choice.startswith('d'):
        try:
            cmd, idx = choice.split(' ')
            # if they try to delete the selected project, reset to None selected
            if project_dirs[int(idx)] == project_name:
                project_name = None
                            
            orchestration_helper.delete_project(project_dirs[int(idx)])
        except:
            print "not a valid choice"
            pause()
            
    else:
        exec_menu(choice, local_menu_actions)
    
    select_project()
    
    return

def get_domain_password():
    global password
    os.system("stty -echo")
    password = raw_input("Enter password [will not echo]")
    os.system("stty echo")
    print "\n"
        
def load_project_data():
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
    
    # we do not store passwords. User must enter it every time they reload a project
    # get_domain_password()
    
def domain_info():
    """
    Load domain data, and convert to OPC format
    """     
    global identity_domain
    global username
    global password
    global image_name
    
    global os_project_name
    global os_image_name    
    
    data_type = "project"
    domain_fields = ["identity_domain", "username", "image_name", "openstack_project", "openstack_image_name"]
    section_name, domain_data = collect_user_input(domain_fields, data_type)
    
    identity_domain = domain_data['identity_domain']
    username = domain_data['username']
    image_name = domain_data['image_name']
    os_project_name = domain_data['openstack_project']
    os_image_name = domain_data['openstack_image_name']
    
    # os.system("stty -echo")
    # password = raw_input("Enter password [will not echo]")
    # os.system("stty echo")
    # print "\n"
    
    # set our name used in compute calls
    global compute_name
    compute_name = "/Compute-" + identity_domain + "/" + username + "/"
    domain_data['compute_name'] = compute_name
    
    section_name = project_name
    orchestration_helper.add_config_section(project_name, data_type, section_name, domain_data)
    
    common_menu_actions['main_menu']()
    return

def common_menu():
    print ""
    print "[m] - Main Menu"
    print "[q] - Quit"

def manage_storage():
    """
    Manage storage objects
    """     
    os.system('clear')
    this_function_name = sys._getframe().f_code.co_name
    print "\t[" + this_function_name + "]\n"
    
    data_type = "storage"
    
    local_menu_actions = {'source_menu': manage_storage,
                          'a': add_storage,
                          'd': "d",
                          'e': 'e'
                         }
    
    local_menu_actions.update(common_menu_actions)
    
    storage_sections = orchestration_helper.get_section_data(project_name, data_type)
    if storage_sections:
        print "Storage already configured:"
        for idx, section in enumerate(storage_sections):
            print "[" + str(idx) + "] " + section
            local_menu_actions[str(idx)] = section
        print ""
    
    print "[a]   - Add Storage"
    print "[d #] - Delete Storage - enter d and the # to delete"
    print "[#]   - Enter number of storage to edit"
    
    handle_manage_input(local_menu_actions, data_type, storage_sections)
    manage_storage()

def add_storage():
    """
    Add storage objects
    """     
    this_function_name = sys._getframe().f_code.co_name
    print "\t[" + this_function_name + "]\n"
    data_type = "storage"
    
    storage_fields = ["name", "properties", "description", "size"]
    section_name, storage_data = collect_user_input(storage_fields, data_type)
    
    if (section_name is None) or (storage_data is None):
        return 
    
    orchestration_helper.add_config_section(project_name, data_type, section_name, storage_data)
    
def handle_manage_input(local_menu_actions, data_type, sections):
    """
    Helper function to handle input from menus
    """     
    common_menu()
    choice = raw_input(" >>  ")
    if choice[:1] in local_menu_actions:
        if choice.isdigit():
            edit_data(local_menu_actions[choice], data_type)
        elif choice.startswith('d'):            
            try:
                cmd, idx = choice.split(' ')
                orchestration_helper.delete_config_section(project_name, data_type, sections[int(idx)])
            except:
                print "not a valid choice"
                pause()
        else:
            exec_menu(choice, local_menu_actions)   
    
    
def edit_data(config_item, data_type):
    """
    Helper for editing data selection from menus
    """     
    print "Editing " + data_type + " item: " + config_item
    print "Press Enter to keep current value. Type new value to change \n"    
    item_data = orchestration_helper.get_config_items(project_name, data_type, config_item)
    for idx , (key, value) in enumerate(item_data):
        print "[" + key + "=" + value + "]"
        choice = raw_input(" >>  ")
        if choice != '':
            orchestration_helper.update_config_section(project_name, data_type, config_item, key, choice)
    return
        
    
def manage_instances():
    """
    Manage instance objects
    """     
    os.system('clear')
    this_function_name = sys._getframe().f_code.co_name
    print "\t[" + this_function_name + "]\n"
    data_type = "instances"
    
    local_menu_actions = {'source_menu': manage_instances,
                          'a': add_instance,
                          'd': "d"
                         }
    local_menu_actions.update(common_menu_actions)
    
    instance_sections = orchestration_helper.get_section_data(project_name, data_type)
    if instance_sections:
        print "Instances already configured:"
        for idx, section in enumerate(instance_sections):
            print "[" + str(idx) + "] " + section
            local_menu_actions[str(idx)] = section
        print ""
    
    print "[a]   - Add Instance"
    print "[d #] - Delete Instance - enter d and the # to delete"
    print "[#]   - Enter number of the instance to edit"
    
    handle_manage_input(local_menu_actions, data_type, instance_sections)
    manage_instances()

def collect_user_input(data_fields, data_type):
    """
    Generic helper to collect input. Pass in a list of fields, and collect a response for each
    """    
    user_data = {}
    section_name = None
    for field in data_fields:
        print "[" + field + "]"
        if field == "properties":
            print "choose either /oracle/public/storage/default or /oracle/public/storage/latency"
        choice = raw_input(" >>  ")
        if field == "name":
            section_name = choice
            full_compute_name = section_name
            section_exists = orchestration_helper.does_name_exist(project_name, data_type, section_name)
            if section_exists:
                print "Name already exists"
                pause()
                return(None, None)
            user_data[field] = full_compute_name
        else:
            user_data[field] = choice    
    return (section_name, user_data)

def select_config_datasource():
    """
    Choose where we will get JSON from for instance config
    """
    config_source = ''
    choice = ''
    while (choice != 'd'):
        print "Enter configSource for this instance"
        print "Leave blank to use defaultJson, or enter data as described in user manual"
        print ""
        print "Current configSource is: " + config_source
        print "[d] - Done"
        choice = raw_input(" >>  ")
        if (choice != 'd'):
            config_source = choice   
        
    return config_source

def select_target_platform():
    """
    Choose target cloud env.
    """ 
    choice = ''
    while (choice != '1') and (choice != '0'):
        print "Select target platform for this instance:"
        print "[0] - Oracle Cloud"
        print "[1] - OpenStack"
        choice = raw_input(" >>  ")   
    
    if (choice == '0'):
        target_platform = "opc"
    elif (choice == '1'):
        target_platform = "openstack"

        
    return target_platform
    
def add_instance():
    """
    Add instance object
    """     
    # os.system('clear')
    this_function_name = sys._getframe().f_code.co_name
    print "\t[" + this_function_name + "]\n"
    data_type = "instances"
    
    instance_fields = ["name", "hostname", "opc_shape", "openstack_flavor", "sshkeyName"]
    section_name, instance_data = collect_user_input(instance_fields, data_type)
    
    if (section_name is None) or (instance_data is None):
        return    

    instance_data['targetPlatform'] = select_target_platform()
    instance_data['configSource'] = select_config_datasource()
    selected_types = select_instance_type()
    instance_data['instanceTypes'] = ",".join(selected_types)
    instance_type_data = instance_type_config.instance_type_config(selected_types)
    instance_data['jsonData'] = json.dumps(instance_type_data)
    selected_storage = add_storage_to_instance(section_name)
    instance_data['attachedStorage'] = ",".join(selected_storage)
    
    
    orchestration_helper.add_config_section(project_name, data_type, section_name, instance_data)

def add_storage_to_instance(section_name):
    """
    Optionally add storage object ref to instance object
    """     
    os.system('clear')
    storage_data_type = "storage"
    instance_data_type = "instances"
    
    local_menu_actions = {}
    storage_to_attach = []
    
    local_menu_actions.update(common_menu_actions)
    
    # list of any storage already in an instance
    attached_storage = orchestration_helper.get_all_attached_storage(project_name, instance_data_type)
    
    # list of all defined storage
    storage_sections = orchestration_helper.get_section_data(project_name, storage_data_type) 

    choice = ''
    while choice != 'd':    
        if storage_sections: 
            print "Add Storage to instance:" + section_name
            for idx, section in enumerate(storage_sections):
                print "[" + str(idx) + "] " + section,
                if section in attached_storage:
                    print " [already attached to instance]"
                elif section in storage_to_attach:
                    print " [selected to be attached]"
                else:
                    print  
                local_menu_actions[str(idx)] = section
            print ""    
    
            print "Select number(s) of Storage to add. [optional]"
            print "[d] - Done selecting storage"
            choice = raw_input(" >>  ")
            if (choice != 'd') and (choice.isdigit()):
                if (int(choice) <= len(storage_sections)):
                    selectedStorage = storage_sections[int(choice)]
                    storage_to_attach.append(selectedStorage)   
        else:
            print "no storage defined"
            print "[d] - Done selecting storage"
            choice = raw_input(" >>  ")
    return storage_to_attach    
    
    
def select_instance_type():
    """
    Select instance type. Used to decide what JSON data is required
    """     
    os.system('clear')
    this_function_name = sys._getframe().f_code.co_name
    print "\t[" + this_function_name + "]\n"
        
    instance_types = [('ATG', 'atg'), ("WebLogic - Admin Server", "weblogic"), ("WebLogic - Managed Server", "weblogicManagedServer"), ("Endeca - all components", "endeca"),
                      ("Endeca - DGraph only", "dgraph"), ("OTD install", "otd"), ("OTD configuration", "otdconfig"), ("Oracle Database", "db")]
    
    selected_types = []
    choice = ''
    while choice != 'd':
        os.system('clear')
        for idx , (key, value) in enumerate(instance_types):
            if value in selected_types:
                print "[" + str(idx) + "] [selected]   " + key
            else:
                print "[" + str(idx) + "] " + key

        print "\n[d] - Done selecting instance types\n"
        print "Select number to toggle instance type"
        choice = raw_input(" >>  ")
        if (choice != 'd') and (choice.isdigit()):
            if (int(choice) <= len(instance_types)):
                (key, value) = instance_types[int(choice)]
                if value in selected_types:
                    selected_types.remove(value)
                else:
                    selected_types.append(value)
                              
    return selected_types

def generate_orchestrations():
    """
    Entry point to generate orchs and ansible yaml
    """     
    orchestration_helper.generate_orchestrations(project_name, identity_domain, username, image_name)
    print "Orchestrations generated"
    pause()
    back()
    return
            
# Back to main menu
def back():
    common_menu_actions['main_menu']()

def pause():
    raw_input("Press Enter to continue...")
    

def progexit():
    print "Exiting"
    sys.exit()

common_menu_actions = {
    'main_menu': main_menu,
    'b': back,
    'm': main_menu,
    'q': progexit
}

if __name__ == "__main__":
    # Launch main menu
    main_menu()

