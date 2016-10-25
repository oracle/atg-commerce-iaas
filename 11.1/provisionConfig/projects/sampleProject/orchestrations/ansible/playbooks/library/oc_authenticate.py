#!/usr/bin/python
# Copyright (c) 2013, 2014-2016 Oracle and/or its affiliates. All rights reserved.

DOCUMENTATION = '''
---
module: oc_authenticate
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
__module__ = "oc_authenticate"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import os
import sys

from oc.authenticate import authenticate as authenticate_occs
from oc.authenticate_oscs import authenticate as authenticate_oscs

# Main processing function
def main():
    module = AnsibleModule(
            argument_spec = dict(
                    endpoint     = dict(required=True, type='str'),
                    user         = dict(required=True, type='str'),
                    password     = dict(required=True, type='str'),
                    storage      = dict(required=False, type='bool', default=False)
            )
    )

    endpoint = module.params['endpoint']
    user = module.params['user']
    password = module.params['password']
    storage = module.params['storage']
    if storage:
        # Authorise against Oracle Storage Cloud
        authtoken, storageurl = authenticate_oscs(endpoint, user, password)
        facts = {'oc_auth_token': authtoken, 'oc_storage_endpoint': storageurl}
    else:
        # Authorise again Oracle Compute Cloud
        cookie = authenticate_occs(endpoint, user, password)
        facts = {'oc_auth_cookie': cookie}

    module.exit_json(changed=True, ansible_facts=facts, cookie=cookie)

    return


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.splitter import *
# Main function to kick off processing
if __name__ == "__main__":
    main()
