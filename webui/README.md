# Provisioning WebUI

The provisioning WebUI provides and interface to manage and generate provisioning configurations, Oracle Cloud orchestrations and Ansible playbooks.
The WebUI is meant to assist with creating the various files needed to use to the IaaS provisioning process.

## Installation
The html and cgi directories need to be accessible to a webserver, such as Apache.
The following are instructions for a default Apache installation on Oracle Linux 6.x. You may need to adjust these instructions for your specific setup.

* Apache should be configured to run as the Oracle user.
* Create the following directories, owned by the Oracle user
  * /var/www/html/controller
  * /var/www/cgi-bin/controller
* Copy the contents of the html directory to /var/www/html/controller (cp html/* /var/www/html/controller)
* Copy the contents of the cgi directory to /var/www/cgi-bin/controller (cp html/* /var/www/cgi-bin/controller)

All files should be owned by the Oracle user.
It is important the Oracle user have permission to write to the cgi-bin tree as this is where the cgi controller scripts will store project configuration data.
When you generate your configuration files, they will be stored in /var/www/cgi-bin/controller/projects

