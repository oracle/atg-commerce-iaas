#!/usr/bin/python
# Copyright (c) 2013, 2014-2016 Oracle and/or its affiliates. All rights reserved.

DOCUMENTATION = '''
---
module: oc_storagevolume
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
        choices: ['create', 'list', 'update', 'delete']
    endpoint:
        description:
            - Oracle Cloud Endpoint
        required: true
        default: null
    user:
        description:
            - Oracle cloud user only required is cookie is not present.
        required: false
        default: null
    password:
        description:
            - Oracle cloud password only required is cookie is not present.
        required: false
        default: null
    cookie:
        description:
            - Oracle cloud authentication cookie.
        required: false
        default: null
    resourcename:
        description:
            - Resource name associated with object we are working with.
        required: false
        default: null
requirements: [oraclecomputecloud]
author: "Andrew Hopkinson (Oracle Cloud Solutions A-Team)"
notes:
    - Simple notes
...
'''

EXAMPLES = '''
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Andrew Hopkinson (Oracle Cloud Solutions A-Team)"
__copyright__ = "Copyright (c) 2013, 2014-2016  Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "oc_storagevolume"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import os
import sys

from oc.authenticate import authenticate
from oc.create_storage_volume import createStorageVolume
from oc.list_storage_volumes import listStorageVolumes
from oc.update_storage_volume import updateStorageVolume
from oc.delete_storage_volume import deleteStorageVolume

# Wait function
def waituntil(endpoint, resourcename, cookie, waitstate, delay=10, retries=120, **kwargs):
    jsonresp = listStorageVolumes(endpoint, resourcename, cookie)
    retry = 0
    success = True
    while 'result' in jsonresp and len(jsonresp['result']) > 0 and jsonresp['result'][0]['status'] != waitstate:
        if retry > retries:
            success =False
            break
        time.sleep(delay)
        jsonresp = listStorageVolumes(endpoint, resourcename, cookie)
        retry += 1
    return success

# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    action         = dict(default='list', choices=['create', 'list', 'update', 'delete']),
                    endpoint       = dict(required=True, type='str'),
                    user           = dict(required=False, type='str'),
                    password       = dict(required=False, type='str'),
                    cookie         = dict(required=False, type='str'),
                    resourcename   = dict(required=True, type='str'),
                    wait           = dict(required=False, type='bool', default=False),
                    waitstate      = dict(required=False, choices=['Online']),
                    waitdelay      = dict(required=False, type='int', default=10),
                    waitretries    = dict(required=False, type='int', default=120),
                    size           = dict(required=False, type='str'),
                    name           = dict(required=False, type='str'),
                    properties     = dict(required=False, type='list', default=['/oracle/public/storage/default']),
                    bootable       = dict(required=False, type='bool', default=False),
                    imagelist      = dict(required=False, type='str'),
                    imagelistentry = dict(required=False, type='str'),
                    description    = dict(required=False, type='str'),
                    tags           = dict(required=False, type='str')
            )
    )

    endpoint = module.params['endpoint']
    user = module.params['user']
    password = module.params['password']
    cookie = module.params['cookie']
    if cookie is None and user is not None and password is not None:
        cookie = authenticate(endpoint, user, password)
    resourcename = module.params['resourcename']
    wait = module.params['wait']
    waitstate = module.params['waitstate']
    waitdelay = module.params['waitdelay']
    waitretries = module.params['waitretries']
    size = module.params['size']
    name = module.params['name']
    bootable = module.params['bootable']
    imagelist = module.params['imagelist']
    imagelistentry = module.params['imagelistentry']
    description = module.params['description']
    tags = module.params['tags']
    properties = module.params['properties']

    changed = True

    if module.params['action'] == 'create':
        jsonobj = createStorageVolume(endpoint, resourcename, cookie, size, name, properties, bootable, imagelist, imagelistentry, description, tags)
        if 'message' in jsonobj and 'already exists' in jsonobj['message']:
            changed = False
        if wait:
            resourcename = name
            if waitstate is None or waitstate == '':
                waitstate = 'Online'
            waituntil(endpoint, resourcename, cookie, waitstate, waitdelay, waitretries)
        module.exit_json(changed=changed, list=jsonobj)
    elif module.params['action'] == 'list':
        jsonobj = listStorageVolumes(endpoint, resourcename, cookie)
        if wait and waitstate is not None and waitstate != '':
            waituntil(endpoint, resourcename, cookie, waitstate, waitdelay, waitretries)
        module.exit_json(changed=changed, list=jsonobj)
    elif module.params['action'] == 'delete':
        jsonobj = deleteStorageVolume(endpoint, resourcename, cookie)
        module.exit_json(changed=changed, list=jsonobj)
    else:
        module.fail_json(msg="Unknown action")

    return


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *
# Main function to kick off processing
if __name__ == "__main__":
    main()
