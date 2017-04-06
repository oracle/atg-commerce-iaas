#!/usr/bin/python
# Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved.

DOCUMENTATION = '''
---
module: oc
short_description: OC External Inventory Script
description:
    Generates inventory that Ansible can understand by making API requests
    Oracle Public Cloud Compute  via a python client used to call the OPC REST services.

    When run against a specific host, this script returns the following variables
    based on the data obtained from the Python REST client:
     - opc_name
     - opc_id
     - opc_status
     - opc_shape
     - opc_image
     - opc_description
     - opc_platform
     - opc_uuid
     - opc_private_ip
     - opc_public_ip
     - opc_nat
     - opc_seclists
     - opc_tags
     - opc_vcable
     - opc_zone
     - opc_instance_orchestration
     - ansible_ssh_host

    When run in --list mode, instances are grouped by the following categories:
     - region:
       region where the current service is located, i.e. us2, em2, em3
     - zone:
       zone group name examples are z26, z26 etc. Zones are bounded to regions
     - instance tags:
       An entry is created for each tag.  For example, if you have two instances
       with a common tag called 'foo', they will both be grouped together under
       the 'tag_foo' name.
     - shape
       types follow based on the shape, like OC1, OC3, OC1M
     - running status:
       group name prefixed with 'status_' (e.g. status_running, status_stopped,..)version_added: ""
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
author: "Andrew Hopkinson / Cristian Anastasiu (Oracle Cloud Solutions A-Team)"
notes:
    - Simple notes
...
'''

EXAMPLES = '''
  Execute uname on all instances in your domain which are in running state
  $ ansible -i oc.py status_running -m shell -a "/bin/uname -a"

  Use the OPC inventory script to print out instance specific information
  $ contrib/inventory/oc.py --host my_instance
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Andrew Hopkinson (Oracle Cloud Solutions A-Team)"
__copyright__ = "Copyright (c) 2013, 2014-2017 Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "Development"
__module__ = "oc"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

__requires__ = ['pycrypto>=2.6']
try:
    import pkg_resources
except ImportError:
    # Use pkg_resources to find the correct versions of libraries and set
    # sys.path appropriately when there are multiversion installs.  We don't
    # fail here as there is code that better expresses the errors where the
    # library is used.
    pass

USER_AGENT_PRODUCT="Ansible-oc_inventory_plugin"
USER_AGENT_VERSION="v1"

import sys
import os
import argparse
import ConfigParser
from time import time

try:
    import json
except ImportError:
    import simplejson as json

class OCInventory(object):

    def _empty_inventory(self):
        return {"_meta": {"hostvars": {}}}

    def __init__(self, refresh_cache=False):
        # Initialise empty inventory
        self.inventory = self._empty_inventory()

        # Read settings and parse args
        self.parse_cli_args()
        self.read_settings()

        # Get REST Connection Driver
        self.driver = Driver()

        # Initialise data
        data_to_print = {}

        # Refresh Cache if stale
        if refresh_cache:
            self.do_api_calls_update_cache()
        elif self.args.refresh_cache:
            self.do_api_calls_update_cache()
        elif not self.is_cache_valid():
            self.do_api_calls_update_cache()


