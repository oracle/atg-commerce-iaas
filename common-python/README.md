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

# baremetal
Libraries to manage Oracle Baremetal Cloud through Ansible - in progress...
 