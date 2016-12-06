#!/usr/bin/python

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

import oraclebmc

DOCUMENTATION = '''
---
module: obmc_instances
short_description: List, create, delete instances in Oracle Baremetal Cloud
extends_documentation_fragment: obmc
version_added: "1.0"
description:
   - List, create, delete instances in Oracle Baremetal Cloud
options:
   name:
     compartment_id:
        - Id of the compartment to use for instances
     required: false
     default: tenancy
   name:
     availability_domain:
        - availability_domain to create instance in
     required: true for creating instances
   name:
     display_name:
        - Display name to use when creating an instance
     required: false
   name:
     metadata:
        - metadata to pass in when creating an instance
     required: false
   name:
     image_id:
        - Id of the image to create instance from
     required: true for creating instances
   name:
     shape:
        - shape of the instance being created
     required: true for creating instances
   name:
     subnet_id:
        - subnet_id for the instance to use
     required: true for creating instances
   name:
     instance_id:
        - instance_id is the id of an instance to delete
     required: true for deleting instances     
requirements:
    - "python >= 2.6"
'''

EXAMPLES = '''
  name: list bmc instances
  tasks:
  - name: list
    obmc_instances:
      action: list
    register: result
  - debug: var=result
  
  name: create bmc instance
  tasks:
  - name: create
    obmc_instances:
      action: create
      display_name: "metatest"
      image_id: ocid1.image.oc1.phx.aaaaaaaan3pu
      shape: BM.Standard1.36
      availability_domain: gMiI:PHX-AD-1
      subnet_id: ocid1.subnet.oc1.phx.aaaaaaaahj
      metadata: {
                "ssh_authorized_keys": "ssh-rsa AAAA.....",
                "script": "/opt/oracle/install/11.1/pywrapper.sh --java --weblogic --weblogicManagedServer"
                   }
                   
  name: delete bmc instance
  tasks:
  - name: delete
    obmc_instances:
      action: delete
      instance_id: ocid1.instance.oc1.phx.abyhqljs7                  
     
'''

def _create_instance(module):
    compartment_id = module.params['compartment_id']
    availability_domain = module.params['availability_domain']
    display_name = module.params['display_name']
    metadata = module.params['metadata']
    image_id = module.params['image_id']
    shape = module.params['shape']
    subnet_id = module.params['subnet_id']
   
    if not availability_domain:
        module.fail_json(msg='availability_domain is required for this command')    
    if not image_id:
        module.fail_json(msg='image_id is required for this command')
    if not shape:
        module.fail_json(msg='shape is required for this command')        
    if not subnet_id:
        module.fail_json(msg='subnet_id is required for this command')

    config = oraclebmc.config.from_file()
    
    compute = oraclebmc.clients.ComputeClient(config)
    
    instance = oraclebmc.models.LaunchInstanceDetails()
    
    if not compartment_id:
        compartment_id = config.get('tenancy')
    
    instance.availability_domain = availability_domain
    instance.compartment_id = compartment_id
    if display_name:
        instance.display_name = display_name
    if metadata:
        instance.metadata = metadata
    instance.image_id = image_id
    instance.shape = shape
    instance.subnet_id = subnet_id
    try:
        launchResponse = compute.launch_instance(instance)        
        jsonobj = oraclebmc.util.to_dict(launchResponse.data)
        module.exit_json(changed=True, instance=jsonobj)
    except Exception as e:
        module.fail_json(msg = str(e))                  

def _list_instances(module):
    
    compartment_id = module.params['compartment_id']
    config = oraclebmc.config.from_file()
    compute = oraclebmc.clients.ComputeClient(config)
    if not compartment_id:
        compartment_id = config.get('tenancy')
    # response comes back as custom bmc model
    modelobj = compute.list_instances(compartment_id)
    # convert custom model to dict
    jsonobj = oraclebmc.util.to_dict(modelobj.data)
    module.exit_json(changed=False, instances=jsonobj) 
    
def _delete_instance(module):
    
    instance_id = module.params['instance_id']
    
    if not instance_id:
        module.fail_json(msg='instance_id is required for this command')    
    config = oraclebmc.config.from_file()
    compute = oraclebmc.clients.ComputeClient(config)
    # response comes back as custom bmc model
    modelobj = compute.terminate_instance(instance_id)
    jsonobj = oraclebmc.util.to_dict(modelobj.data)
    module.exit_json(changed=True, instances=jsonobj)           
    
# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action               = dict(default='list', choices=['create', 'list', 'delete']),
                    compartment_id     = dict(required=False, type='str'),
                    availability_domain  = dict(required=False, type='str'),
                    display_name         = dict(required=False, type='str'),
                    metadata             = dict(required=False, type='dict'),
                    image_id             = dict(required=False, type='str'),
                    shape                = dict(required=False, type='str'),
                    subnet_id            = dict(required=False, type='str'),
                    instance_id          = dict(required=False, type='str')
            )
    )
        
    if module.params['action'] == 'list':
        _list_instances(module)
    elif module.params['action'] == 'delete':
        _delete_instance(module)
    elif module.params['action'] == 'create':
        _create_instance(module)        
    else:
        module.fail_json(msg="Unknown action")

    return


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *
# Main function to kick off processing
if __name__ == "__main__":
    main()
