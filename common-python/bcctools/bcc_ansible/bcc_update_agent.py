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
__module__ = "update_agent"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: bcc_update_agent
short_description: Update agent
version_added: "1.0"
description:
    - Update an agent
options:
    action:
        description:
            - Action to be executed against the BCC
        required: false
        default: update_agent
        choices: ['update_agent']
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
    agentDisplayName:
        description:
            - Name of new agent
        required: false
        default: null
        type: str
    agentDescription:
        description:
            - Description of new agent
        required: false
        default: ""
        type: str
    excludeAssetDestinations:
        description:
            - Assets to exclude from this agent. Comma separated values.
        required: false
        default: ""
        notes: Example - "/atg/epub/file/ConfigFileSystem,/atg/epub/file/WWWFileSystem"
        type: str
    includeAssetDestinations:
        description:
            - Assets to include for this agent. Comma separated values.
        required: false
        default: ""
        notes: Example - "/atg/epub/file/ConfigFileSystem,/atg/epub/file/WWWFileSystem"
        type: str
    agentEssential:
        description:
            - Is this an essential agent?
        required: false
        default: False
        type: bool
    transportURL:
        description:
            - Transport URL for the agent
        required: true
        default: null
        type: str
    targetID:
        description:
            - Target ID to add this agent to
        required: true
        default: null
        type: str
    agentID:
        description:
            - Agent ID to update
        required: true
        default: null
        type: str                                                                                  
requirements:
    - "python >= 2.6"
    - "ATG BCCTools module"
...
'''

EXAMPLES = '''
- name: Update an agent
    bcc_update_agent:
      action: update_agent
      cookie: "{{ session_data.session_cookie }}"
      endpoint: "{{ lookup('env','BCC_ENDPOINT') }}"
      agentDisplayName: "TestAgent2"
      agentEssential: True
      transportURL: "rmi://localhost:8001"
      includeAssetDestinations: "/atg/epub/file/ConfigFileSystem,/atg/epub/file/WWWFileSystem"
      targetID: "{{ targetresult.target.targetDef.ID }}"
      agentID: "{{ agentresult.agentID.agentId }}"
'''

from bcc_rest.bcc_update_agent import updateAgent
 


# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action                      = dict(default='update_agent', choices=['update_agent']),
                    endpoint                    = dict(required=True, type='str'),
                    agentDisplayName            = dict(required=True, type='str'),
                    agentDescription            = dict(required=False, type='str', default=''),
                    excludeAssetDestinations    = dict(required=False, type='str', default=''),
                    includeAssetDestinations    = dict(required=False, type='str', default=''),
                    delimitedDestinationMap     = dict(required=False, type='str', default=''),
                    agentEssential              = dict(required=False, type='bool', default=False),
                    transportURL                = dict(required=True, type='str'),
                    targetID                    = dict(required=True, type='str'),
                    agentID                     = dict(required=True, type='str'),
                    cookie                      = dict(required=False, type='str')
            )
    )

    endpoint = module.params['endpoint']
    agentDisplayName = module.params['agentDisplayName']
    agentDescription = module.params['agentDescription']
    excludeAssetDestinations = module.params['excludeAssetDestinations']
    includeAssetDestinations = module.params['includeAssetDestinations']
    delimitedDestinationMap = module.params['delimitedDestinationMap']
    agentEssential = module.params['agentEssential']
    transportURL = module.params['transportURL']
    targetID = module.params['targetID']
    agentID = module.params['agentID']
    cookie = module.params['cookie']
    
    changed = False

    try:
        if module.params['action'] == 'update_agent':
            response = updateAgent(endpoint, agentDisplayName, agentDescription, excludeAssetDestinations, includeAssetDestinations, delimitedDestinationMap, agentEssential, transportURL, targetID, agentID, cookie)
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
