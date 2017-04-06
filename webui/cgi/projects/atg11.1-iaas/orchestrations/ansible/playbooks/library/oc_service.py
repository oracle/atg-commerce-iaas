#!/usr/bin/python
# Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved.

DOCUMENTATION = '''
---
module: oc_service
short_description: Short Desc
description:
    - Long Desc
version_added: ""
options:
    action:
        description:
            - Action to be executed against the oracle cloud object
        required: false
        default: list
        choices: ['create', 'list', 'delete']
    endpoint:
        description:
            - Oracle Cloud Endpoint
        required: true
        default: null
    user:
        description:
            - Oracle cloud user.
        required: true
        default: null
    password:
        description:
            - Oracle cloud password.
        required: true
        default: null
requirements: [oraclecomputecloud]
author: "Michael Shanley (Oracle A-Team)"
notes:
    - Simple notes
...
'''

EXAMPLES = '''
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Michael Shanley (Oracle A-Team)"
__copyright__ = "Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "oc_service"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import os
import sys
import json
import time

from oc.create_service import createDbcs
from oc.list_service import listService
from oc.delete_service import deleteDbcs
from oc.connection import PSMConnection

# Wait function
def waituntil(psmConn, name, waitstate, delay=10, retries=120, **kwargs):
    jsonresp = listService(psmConn, name)
    retry = 0
    success = True
    while 'status' in jsonresp and len(jsonresp['status']) > 0 and jsonresp['status'] != waitstate:
        if retry > retries:
            success =False
            break
        time.sleep(delay)
        jsonresp = listService(psmConn, name)
        retry += 1
    return success

# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action         = dict(default='list', choices=['add', 'create', 'list', 'delete', 'start', 'stop']),
                    endpoint   = dict(required=True, type='str'),
                    user           = dict(required=False, type='str'),
                    password       = dict(required=False, type='str'),
                    tenant         = dict(required=False, type='str'),
                    service        = dict(required=False, type='str'),
                    payload        = dict(required=False, type='str'),
                    name           = dict(required=False, type='str'),
                    wait           = dict(required=False, type='bool', default=False),
                    waitstate      = dict(required=False, choices=['Running', 'Stopped', 'Failed']),
                    waitdelay      = dict(required=False, type='int', default=10),
                    waitretries    = dict(required=False, type='int', default=120)
            )
    )

    endpoint = module.params['endpoint']
    user = module.params['user']
    tenant = module.params['tenant']
    service = module.params['service']
    password = module.params['password']
    payload = module.params['payload']
    name = module.params['name']
    wait = module.params['wait']
    waitstate = module.params['waitstate']
    waitdelay = module.params['waitdelay']
    waitretries = module.params['waitretries']
    if payload is not None:
        payload = payload.replace("'", '"')

    changed = False
    jsonobj = module.params

    try:
        psmConn = PSMConnection(endpoint, user, password, service, tenant)
        if module.params['action'] == 'create' or module.params['action'] == 'add':
            code, text = createDbcs(psmConn, payload)
            if code == 202:
                changed = True
            module.exit_json(changed=changed, list=code)
        elif module.params['action'] == 'list':
            jsonobj = listService(psmConn, name)          
            module.exit_json(changed=changed, list=jsonobj)
        elif module.params['action'] == 'delete':
            jsonobj = deleteDbcs(psmConn, name)
            module.exit_json(changed=changed, list=jsonobj)
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
