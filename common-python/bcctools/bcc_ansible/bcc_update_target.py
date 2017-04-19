#!/usr/bin/python

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
__copyright__ = "Copyright (c) 2017 Oracle"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "update_target"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: bcc_update_target
short_description: Update target
version_added: "1.0"
description:
    - Update a target
options:
    action:
        description:
            - Action to be executed against the BCC
        required: false
        default: update_target
        choices: ['update_target']
    endpoint:
        description:
            - BCC REST Endpoint
        required: true
        default: null
        type: str
    cookie:
        description:
            - ATG Cookie
        required: false
        default: null
        type: str
    targetName:
        description:
            - Name of new target
        required: true
        default: null
        type: str
    description:
        description:
            - Description of new target
        required: false
        default: ""
        type: str
    flagAgents:
        description:
            - Flag agents only - do not deploy to target
        required: false
        default: False
        type: bool
    targetOneOff:
        description:
            - Is this a one off target?
        required: false
        default: False
        type: bool
    delimitedRepositoryMappings:
        description:
            - Mapping for source and destination repositories for this target.
              Source and destination repositories are separated by $$. Each mapping item is comma separated.
        required: false
        default: ""
        type: str
    targetID:
        description:
            - ID of the target to update
        required: true
        default: null
        type: str        
requirements:
    - "python >= 2.6"
    - "ATG BCCTools module"
...
'''

EXAMPLES = '''
- name: Update target
    bcc_update_target:
      action: update_target
      cookie: "{{ session_data.session_cookie }}"
      endpoint: "{{ lookup('env','BCC_ENDPOINT') }}"
      targetName: "TestChange"
      delimitedRepositoryMappings: "/atg/userprofiling/PersonalizationRepository$$/atg/userprofiling/PersonalizationRepository_production"
      targetID: "{{ targetresult.target.targetDef.ID }}"
'''

from bcc_rest.bcc_update_target import updateTarget
 


# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action                      = dict(default='update_target', choices=['update_target']),
                    endpoint                    = dict(required=True, type='str'),
                    targetName                  = dict(required=True, type='str'),
                    description                 = dict(required=False, type='str', default=''),
                    flagAgents                  = dict(required=False, type='bool', default=False),
                    targetOneOff                = dict(required=False, type='bool', default=False),
                    delimitedRepositoryMappings = dict(required=False, type='str', default=''),
                    targetID                    = dict(required=True, type='str'),
                    cookie                      = dict(required=False, type='str')
            )
    )

    endpoint = module.params['endpoint']
    targetName = module.params['targetName']
    description = module.params['description']
    flagAgents = module.params['flagAgents']
    targetOneOff = module.params['targetOneOff']
    delimitedRepositoryMappings = module.params['delimitedRepositoryMappings']
    targetID = module.params['targetID']
    cookie = module.params['cookie']
    
    changed = False

    try:
        if module.params['action'] == 'update_target':
            response = updateTarget(endpoint, targetName, description, flagAgents, targetOneOff, delimitedRepositoryMappings, targetID, cookie)
            jsonobj = json.loads(response.text)
            if ('formExceptions' in jsonobj) :
                module.fail_json(msg=jsonobj)            
            module.exit_json(changed=changed, target=jsonobj)
        else:
            module.fail_json(msg="Unknown action")
    except Exception as e:
        module.fail_json(msg=str(e.message))

    return


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *

# Main function to kick off processing
if __name__ == "__main__":
    main()
