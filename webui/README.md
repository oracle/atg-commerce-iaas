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

### Set ATG version template
In the orch_templates folder, there is a master json template called json.template. The contents of this file are what determine the required fields and values for instance configuration. The default file is set to ATG 11.1.
To change this to a ATG 11.2 template, copy json11.2.template to json.template.
To change back to ATG 11.1, copy json11.1.template to json.template.

* note - there is a problem with orchestration generation in ATG 11.2. common-python/oc_provisioning/oc_provision_config/orchestration_helper_webui.py has the path to the 11.1 pywrapper hard coded. This will be fixed and made configurable soon.


