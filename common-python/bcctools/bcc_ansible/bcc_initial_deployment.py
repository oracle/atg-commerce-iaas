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
__module__ = "initial_deployment"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: bcc_initial_deployment
short_description: Start the first deployment on a new site
version_added: "1.0"
description:
    - Start the first deployment on a new site
options:
    action:
        description:
            - Action to be executed against the BCC
        required: false
        default: initial_deployment
        choices: ['initial_deployment']
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
    targetID:
        description:
            - ID of the target you want to deploy to
        required: true
        default: null
        type: str
    flagAgents:
        description:
            - Flag agents only - do not do a full deploy
        required: false
        default: False
        type: bool                 
requirements:
    - "python >= 2.6"
    - "ATG BCCTools module"
...
'''

EXAMPLES = '''
'''

from bcc_rest.bcc_initial_deployment import initialDeployment
 
# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action          = dict(default='initial_deployment', choices=['initial_deployment']),
                    endpoint        = dict(required=True, type='str'),
                    targetID        = dict(required=True, type='str'),
                    flagAgents      = dict(required=False, type='bool', default=False),
                    cookie          = dict(required=False, type='str')
            )
    )

    endpoint = module.params['endpoint']
    targetID = module.params['targetID']
    flagAgents = module.params['flagAgents']
    cookie = module.params['cookie']
    
    changed = False

    try:
        if module.params['action'] == 'initial_deployment':
            response = initialDeployment(endpoint, targetID, flagAgents, cookie)
            jsonobj = json.loads(response.text)
            
            if ('formExceptions' in jsonobj):
                module.fail_json(msg=jsonobj)
                           
            module.exit_json(changed=changed, targetID=jsonobj)
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
