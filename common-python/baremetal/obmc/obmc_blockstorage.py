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
module: obmc_images
short_description: List images in Oracle Baremetal Cloud
extends_documentation_fragment: obmc
version_added: "1.0"
description:
   - List images in Oracle Baremetal Cloud
options:
   name:
     compartment_id:
        - Id of the compartment to list images from
     required: false
     default: tenancy
requirements:
    - "python >= 2.6"
'''

EXAMPLES = '''
  - name: list
    obmc_images:
      action: list
    register: result
  - debug: var=result
'''


def _list_storage(module):
    
    compartment_id = module.params['compartment_id']
    config = oraclebmc.config.from_file()
    #compute = oraclebmc.clients.ComputeClient(config)
    storage = oraclebmc.clients.BlockstorageClient(config)
    if not compartment_id:
        compartment_id = config.get('tenancy')
    # response comes back as custom bmc model
    modelobj = storage.list_volumes(compartment_id)
    # convert custom model to dict
    jsonobj = oraclebmc.util.to_dict(modelobj.data)
    module.exit_json(changed=False, volumes=jsonobj)   
    
    
# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action               = dict(default='list', choices=['list']),
                    compartment_id     = dict(required=False, type='str')
            )
    )
        
    if module.params['action'] == 'list':
        _list_storage(module)     
    else:
        module.fail_json(msg="Unknown action")

    return


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *
# Main function to kick off processing
if __name__ == "__main__":
    main()
