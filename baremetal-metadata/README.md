# Baremetal metadata reader

The included python script allows a custom VM image to read user provided metadata from OpenStack at VM boot time.
The code allows the instance to automatically execute code the first time it boots up.
This code is the entry point into the provisioning process on OpenStack, and is much like opc-init on Oracle Public Cloud.

## Installation
* Copy opc-bmc-init to /etc/init.d
* Edit opc-bmc-init to use the correct python interpreter for your setup, and to point to the correct pywarpper.sh entry point.
* Make sure opc-bmc-init has execute permissions
* Add opc-bmc-init to your systems boot process
  * Add /etc/init.d/opc-bmc-init to /etc/rc.local
  
 
## Usage
The load_barmetal_userdata.py script reads metadata from baremetal.
It looks for the key "script". If present, it execute the value of the key as a shell script.
The userdata field is expected to be in JSON format.

Example:
{"script": "/opt/oracle/install/11.1/pywrapper.sh --java"}

