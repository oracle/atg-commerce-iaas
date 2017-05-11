# Oracle ATG Commerce Sample Orchestrations

These files are sample Oracle Public Cloud orchestrations meant to be used with the Oracle ATG Commerce cloud provisioning process.
These orchestrations, once properly edited and added to your OPC domain, will create a demo ATG cluster for you.

## Installation

Create your own image using the provisioning code in this repository, or, obtain a sample image from the Oracle Cloud Marketplace.

Edit all files. (a text editor like notepad++ will allow you to edit all files at one time, doing a global find and replace)
* Replace DOMAINNAME with your Oracle Public Cloud domain name
* Replace USERNAME with your Oracle Public Cloud login, which is typically your email address.
* Replace SSHKEYNAME with the name of the SSH key you want injected into each instance that is provisioned. You must setup this key up in your OPC domain prior to running these orchestrations.

Different top level(nested) orchestrations are provided; one to start an ATG 11.1 environment, one for ATG 11.2, and another for ATG 11.3.  
These use either the commerce_instances_11_1, commerce_instances_11_2, or commerce_instances_11_3 orchestration file.  

In the commerce_instances_11_x files, there is a pointer to the custom image name that was obtained from the Oracle Cloud Marketplace. Make sure this name matches the name of the image as it appears on the images tab of your compute console.  
For example:  
"imagelist": "/Compute-mydemodomain/john.jones@example.com/atg11_1_v15"  
This would mean you have a private image in your OPC domain with the name atg11_1_v15  

Upload all files to the orchestrations tab of your OPC domain.  
Upload the nested orchestration files last, or you will get an error. Because this orchestration makes reference to all the other orchestrations, they must exist or the nested orchestration will fail a validation check.  

### Filled in example
The following is a block from the commerce_instances file with DOMAINNAME, USERNAME and SSHKEYNAME replaced with sample data.
```
               {
                    "instances": [
                        {
                            "imagelist": "/Compute-mydemodomain/john.jones@example.com/atg11_1_v15",
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
                                    "nat": "ippool:/oracle/public/ippool"
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
With your private image, and orchestrations in place in your OPC domain, go to the orchestrations tab and start the orchestration with the description "RUN ME - Commerce Stack Setup 11.x", where x is the version of the stack you want to startup. 

Do not attempt to start multiple stacks at the same time, they will colide with each other.  
This is a top level, nested orchestartion that will start all other orchestration files in the correct order.

To remove the ATG demo setup, simply stop the orchestration with the description "RUN ME - Commerce Stack Setup 11.x". This will delete all elements that were created by the nested orchestrations.
