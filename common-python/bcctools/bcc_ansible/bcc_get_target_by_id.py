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
__module__ = "get_target_by_id"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: bcc_get_target_by_id
short_description: Get a target by ID
version_added: "1.0"
description:
    - Get a target by ID
options:
    action:
        description:
            - Action to be executed against the BCC
        required: false
        default: get_target_by_id
        choices: ['get_target_by_id']
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
            - ID of the target you want returned
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

from bcc_rest.bcc_get_target_by_id import getTarget
 
# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action          = dict(default='get_target', choices=['get_target']),
                    endpoint        = dict(required=True, type='str'),
                    targetID        = dict(required=True, type='str'),
                    cookie          = dict(required=False, type='str')
            )
    )

    endpoint = module.params['endpoint']
    targetID = module.params['targetID']
    cookie = module.params['cookie']
    
    changed = False

    try:
        if module.params['action'] == 'get_target':
            response = getTarget(endpoint, targetID, cookie)
            jsonobj = response.text
            if ('error' in jsonobj):
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
