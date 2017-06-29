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
__module__ = "get_agent_by_name"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: bcc_get_agent_by_name
short_description: Get an agent by name
version_added: "1.0"
description:
    - Get an agent based on target name and agent name
options:
    action:
        description:
            - Action to be executed against the BCC
        required: false
        default: get_agent_id
        choices: ['get_agent_id']
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
            - Name of the target the agent you want is tied to
        required: true
        default: null
        type: str
    agentName:
        description:
            - Name of the agent you want returned
        required: true
        default: null
        type: str       
requirements:
    - "python >= 2.6"
    - "ATG BCCTools module"
...
'''

EXAMPLES = '''
'''

from bcc_rest.bcc_get_agent_by_name import getAgent
 
# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action          = dict(default='get_agent_by_name', choices=['get_agent_by_name']),
                    endpoint        = dict(required=True, type='str'),
                    targetName      = dict(required=True, type='str'),
                    agentName       = dict(required=True, type='str'),
                    cookie          = dict(required=False, type='str')
            )
    )

    endpoint = module.params['endpoint']
    targetName = module.params['targetName']
    agentName = module.params['agentName']
    cookie = module.params['cookie']
    
    changed = False

    try:
        if module.params['action'] == 'get_agent_by_name':
            response = getAgent(endpoint, targetName, agentName, cookie)
            jsonobj = json.loads(response.text)
            if ('error' in jsonobj):
                module.fail_json(msg=jsonobj)             
            module.exit_json(changed=changed, agent=jsonobj)
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
