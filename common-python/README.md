# Common python libraries

# oc_provisioning
oc_provisioning contains python dependencies for the IaaS provisioning process, and for the WebUI tool.

## Installation
cd to the oc_provisioning directory and execute:
python setup.py install

Make sure the user you execute this as has permissions to write to your python library area - you may need to be root.
If you are using a python interpreter other than the default python command, such as python2.7, adjust the command accordingly.


# rest_wrappers
rest_wrappers contains python dependencies to allow Ansible to call Oracle Cloud REST api's.

## Installation
cd to the rest_wrappers/oc directory and execute:
python setup.py install

Make sure the user you execute this as has permissions to write to your python library area - you may need to be root.
If you are using a python interpreter other than the default python command, such as python2.7, adjust the command accordingly.

# bcctools
bcctools/bcc_rest contains python libraries to allow making REST calls into ATG Content Administration (the BCC).
bcctools/bcc_ansible contains python libraries to allow Ansible to leverage the bcc_rest libraries.
bcctools/sample-playbooks contains sample Ansible playbooks making use of bcc_rest and bcc_ansible.

## Installation
Refer to bcctools/README.md

# baremetal
Libraries to manage Oracle Baremetal Cloud through Ansible - in progress...
 