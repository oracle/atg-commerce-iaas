# OpenStack metadata reader

The included python script allows a custom VM image to read user provided metadata from OpenStack at VM boot time.
The code allows the instance to automatically execute code the first time it boots up.
This code is the entry point into the provisioning process on OpenStack, and is much like opc-init on Oracle Public Cloud.

## Installation
* Copy opc-solaris-init to /etc/init.d
* Edit opc-solaris-init to use the correct python interpreter for your setup, and to point to the correct pywarpper.sh entry point.
* Add opc-solaris-init to your systems boot process
  * Create start/stop links in /etc/rc3.d pointing to the /etc/init.d/opc-solaris-init
  * OR Create a Solaris SMF service that calls opc-solaris-init
  
 
## Usage
The load_openstack_userdata.py script reads the userdata field from OpenStack metadata.
It looks for the key "script". If present, it execute the value of the key as a shell script.
The userdata field is expected to be in JSON format.

Example:
{"script": "/opt/oracle/install/11.1/pywrapper.sh --java"}

