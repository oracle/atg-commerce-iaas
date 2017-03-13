# Oracle ATG Commerce Sample Orchestrations

These files are sample Oracle Public Cloud orchestrations meant to be used with the Oracle ATG Commerce cloud provisioning process.
These orchestrations, once properly edited and added to your OPC domain, will create a demo ATG cluster for you.

## Installation

Create your own image using the provisioning code in this repository, or, obtain a sample image from the Oracle Cloud Marketplace.

Edit all files.
Replace DOMAINNAME with your Oracle Public Cloud domain name
Replace USERNAME with your Oracle Public Cloud login, which is typically your email address.
Replace SSHKEYNAME with the name of the SSH key you want injected into each instance that is provisioned. You must setup this key up in your OPC domain prior to running these orchestrations.
If your private OPC image name is not atg11_1_p1, replace all occurrences of that string in the commerce_instances file with the name of the private image you wish to use.

Upload all files to the orchestrations tab of your OPC domain.



### Filled in example
The following is a block from the commerce_instances file with DOMAINNAME, USERNAME and SSHKEYNAME replaced with sample data.
```
               {
                    "instances": [
                        {
                            "imagelist": "/Compute-mydemodomain/john.jones@example.com/atg11_1_p1",
                            "label": "endeca1",
                            "name": "/Compute-mydemodomain/john.jones@example.com/endeca1",
                            "tags": [
                                "endeca1"
                            ],
                            "hostname": "endeca1",
                            "shape": "oc2m",
                            "networking": {
                                "eth0": {
                                    "seclists": [
                                        "/Compute-mydemodomain/john.jones@example.com/endeca_instances",
                                        "/Compute-mydemodomain/john.jones@example.com/endeca1_server",
                                        "/Compute-mydemodomain/default/default"
                                    ],
                                    "nat": "ipreservation:/Compute-mydemodomain/john.jones@example.com/endeca1"
                                }
                            },
                            "sshkeys": [
                                "/Compute-mydemodomain/john.jones@example.com/jjoneskey"
                            ],
                            "attributes": {
                                "userdata": {
                                    "pre-bootstrap": {
                                        "script": "/opt/oracle/install/11.1/pywrapper.sh --endeca --copy-ssh-keys"
                                    }
                                }
                            }
                        }
```

## Usage
With your private image, and orchestrations in place in your OPC domain, go to the orchestrations tab and start the orchestration with the description "RUN ME - Commerce Stack Setup".
This is a top level, nested orchestartion that will start all other orchestration files in the correct order.

To remove the ATG demo setup, simply stop the orchestration with the description "RUN ME - Commerce Stack Setup". This will delete all elements that were created by the nested orchestrations.

