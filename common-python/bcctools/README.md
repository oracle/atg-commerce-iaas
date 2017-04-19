# BCC Tools
These python libraries are REST wrappers and Ansible wrappers to allow management of ATG Content Administration, A.K.A the BCC, to be managed remotely via REST services.

# Prerequisites
You must have the BCCTools ATG module installed and running. This is the code that these python wrappers calls in to.  

You must have python 2.6 or greater installed to use the REST and Ansible wrappers.  

# Installation

## Install REST wrappers
From the root bcctools folder, execute:  
python setup.py install  

Change python to match your python executable if not using the default.

## Configure Ansible
In the sample-playbooks folder, edit ansible_hosts.
Change ansible_python_interpreter to match the path to your python executable. This must be the same python you used to install the REST wrappers.  

In the sample-playbooks folder, edit ansible.cfg.  
Change the log_path to match where you would like Ansible log files to be written.  

By default, the Ansible wrappers are pulled in from, relative to the playbooks, ../bcc_ansible.  
You can place these where ever you like, as long as your library path in ansible.cfg points to them.  


## Configure environment variables
The Ansible playbooks require several environment variables to properly execute.
A sample set_bcc_env file is provided with sample values.  

The environment variables required are:  
BCC_ENDPOINT - This is the URL to your BCC instance. This is the endpoint REST calls will be made to.  
BCC_USER - This is the user you want to authenticate against the BCC with.  
BCC_PASSWORD - This is the password for your BCC_USER  
ANSIBLE_INVENTORY - This is the path to your ansible_hosts file  

# Usage
The REST API's are configured with security enabled by default. 
This required that you perform 2 tasks at the start of every REST call:
1. Get an ATG session confirmation number (_dynSessConf)
2. Login in with a valid BCC user and password, tied to the session you obtained in step 1.

## Sample Session and Login
The following is the contents of the bcc_login.yaml playbook, with explanations of some steps.
```
  - name: Get Session Confirmation
    # we need a valid session conf before we can do anything else
    bcc_session_confirmation:
      action: get_session
      endpoint: "{{ lookup('env','BCC_ENDPOINT') }}"
    # save the result in session_data
    register: session_data
    
  - name: Login
    bcc_login:
      action: login
      # session_data set in bcc_session_confirmation contains the cookie data we need
      cookie: "{{ session_data.session_cookie }}"
      # get login credentials from environment variables
      username: "{{ lookup('env','BCC_USER') }}"
      password: "{{ lookup('env','BCC_PASSWORD') }}"
      endpoint: "{{ lookup('env','BCC_ENDPOINT') }}"
```
* bcc_session_confirmation - This calls the bcc_session_confirmation code, and returns _dynSessConf and a JSESSIONID, stored in the session_data variable
* "{{ lookup('env','BCC_ENDPOINT') }}" - This looks up the value of your BCC_ENDPOINT environment variable
* register: session_data - This stores the output of bcc_session_confirmation in the session_data variable
* cookie: "{{ session_data.session_cookie }}" - The session_data variable obtained by bcc_session_confirmation holds the cookie data you must use on all REST calls. When you login, the JSESSIONID in the cookie is used to persist the elevated security status of the authenticated user between REST calls.

Every playbook should begin with getting a session confirmation number, and logging a user in. Without this, your REST calls will fail due to unauthorized access.

## Importing a topology
You can import an existing topology. Yout topology XML data must be converted to a base64 string, with no line wraps. This string is what is passed to the REST API.  
On unix/linux, to convert a file to base64 with no wraps, execute:
* base64 --wrap=0 deploymentTopology.xml > base64Topology

Refer to the sample bcc_import_topology playbook for an example of how to load the data directly from the file system.

## Accessing targets and agents
Targets and Agents must be manipulated by ID.
Helper services are provided that allow you to get the ID of a target or agent based on a name. See the sample playbooks for details.

## Sample playbooks
Sample Ansible playbooks are provided to demonstrate various tasks with the REST api's.
The sample playbooks, and Ansible modules in the bcc_ansible tree contain additional embedded documentation.

Not all the sample playbooks will run successfully on their own. They are provided to show example of various functions.   
The playbook bcc_add_complete_site.yaml is an entire process that will create a new target, add agents to it, and make the changes live.  

# Module Documentation
See ANSIBLE-MODULES.md for complete module docs  

