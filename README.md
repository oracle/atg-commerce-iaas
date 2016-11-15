# Oracle ATG Commerce IaaS provisioning

# Introduction
The Oracle ATG Commerce provisioning tool set allows for the rapid deployment of the ATG Commerce stack.
In the x86 Oracle Public Cloud and Oracle SPARC cloud, the entire provisioning, installation and configuration process takes roughly 20-25 minutes. The end result is a complete Oracle ATG Commerce Stack installed, with base configuirations, ready to go.

The tool set contains 3 distinct components that can be used independently, or together to create a Cloud provisioning, software installation and software configuration solution.

The Oracle ATG Commerce stack is comprised of several integrated software packages. The provisioning tool set allows the end user to control the following products:
* Oracle ATG Commerce
* WebLogic
* Endeca
* Java
* Oracle Database
* Oracle Traffic Director
 
# Process overview
The provisioning process is driven by JSON templates that define how software is to be installed and configured. You can have as few, or as many templates as desired; with each defining a specific environment setup.

For example, you may have one template that defines a development setup, another that defines a QA/test environment, and another that defines a production environment.

The templates allow for a repeatable, consistent deployment of the Commerce stack.

# Overview of the tools
All tools are written in Python, and are published under the MIT license.

The tools have been written and tested against Solaris SPARC and Oracle Linux, but will likely work on any flavor of Linux/Unix with an appropriate Python interpreter.

## Cloud provisioning
The tools utilize REST api's provided by Oracle OpenStack for SPARC provisioning, and the public API's provided by Oracle Public Cloud for x86 provisioning.

The tools handle provisioning through either Oracle Cloud Orchestrations, or Ansible playbooks.

This is the first step of the process that creates the actual server instances and associated storage for each instance.

## Software installation and configuration
After a server instance has been provisioned, the installation and configuration of software is automatically started.

Your templates define what software will be installed on which specific server, and how that software will be configured.

The installation and configuration process can also be run by itself. For example, if you wanted to setup a local developer VM, you can install and configure the entire Commerce stack with a single command.

## Template and playbook generator
The tool set also includes an interface that assists with the generation of JSON templates, Cloud Orchestrations and Ansible playbooks.

The configuration generator helps guide the user through all the information required for the templates, orchestrations and playbooks. Once all data has been entered, the tools generates orchestrations and playbooks for you. Generated files automatically use the correct REST api's and Cloud endpoints based on user input.

# Tool features
Some of the features in the tool set include:
* Install ATG
    * Optionally install ATG patches
* Install Java
* Install Endeca
* Install and Configure WebLogic
    * Create managed servers
 	* Create instances with host/port bindings
 	* Create and bind datasources to instances<
 	* Generate ATG server layers for each instance
 	* Generate start/stop scripts
    * Optionally install WebLogic patches
* Install and Configure Oracle Traffic Director
* Install Oracle Database, and create a new starter database instance

# Components
* common_python contains the python libraries for the provisioning services, and REST api wrappers to talk to OpenStack and Oracle Public Cloud.
* iaas-11.1 contains the entry point to install and configure the Oracle ATG Commerce 11.1 stack
* iaas-11.2 contains the entry point to install and configure the Oracle ATG Commerce 11.2 stack
* webui contains the WebUI tool for assist in generating configuration data and Ansible playbooks.
* openstack-metadata contains a script to retrieve user metadata from OpenStack.

## Additional instructions
Installation and additional instructions are contained in each top level folder.

# Contributing

See
[CONTRIBUTING](https://github.com/oracle/atg-commerce-iaas/tree/master/CONTRIBUTING.md)
for details.



