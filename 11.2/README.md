# Oracle ATG Commerce 11.2 IaaS provisioning

This area contains the files required to automate the installation and configuration of the Oracle ATG Commerce 11.2 stack on Oracle Compute Cloud, Oracle SPARC Cloud/OpenStack, or locally servers/VM's.

## Installation
This code required the oc_provisioning wrappers to be installed in your python distribution.
Go to the common_python/oc_provisioning directory and follow the installation instructions prior to use.

If you wish to use Ansible to control provisioning, you must also install the rest_wrappers.
Go to the common_python/rest_wrappers directory and follow the installation instructions prior to use.

Before use, check the python interpreter specified at the top of commerce_setup.py
By default, it is set to use /usr/bin/python2.7
If you are installing the library dependencies into another python installation, adjust this line accordingly.

## Detailed usage
Detailed usage instructions are contained in the PDF manual included with the code.

## Performance and tuning considerations
The following are some best practices and tuning tips for Oracle Cloud.  
Your individual needs will vary based on your specific application configuration. These are some tips that can assist with tuning your Commerce implementation on Oracle Cloud.  

http://www.oracle.com/webfolder/technetwork/tutorials/ohc/E83035_01.pdf

