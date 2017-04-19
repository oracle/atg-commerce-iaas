# ATG BCCTools module

This is a module for Oracle ATG Commerce that provides REST services for interacting with ATG Content Administration, a.k.a, the BCC.

# Installation

## Building code
You can optionally build the code yourself, a maven build file is provided.  
To utilize this build, your maven repository must have the appropriate ATG product libraries.  
A shell script is provided, install-atglibs-maven.sh, that will place many of the most commonly used libraries into your maven repository, and name them the way the provided maven build expects them to be.  
You must have the DYNAMO_ROOT environment variable set properly, pointing to the root of your ATG installation.  
The sample build file and library shell script are setup for ATG 11.1. You will need to modify them for use with any other version of ATG.  

Building the code will create the BCCTools module in DYNAMO_ROOT/BCCTools

## Provided module
A prebuilt module is provided in the compiled-module directory.  
This module was built with Java 1.7.  
To use this module, copy the BCCTools directory from compiled-module to your dynamo root.

## Included BCCTools in your application ear.
You must include the BCCTools ATG module in your application ear that you install in your Content Administration ATG instance.  
When calling runAssembler, add the BCCTools module to your list of modules.  

# Usage
There are 3 primary ways to utilize this module.  
1. Build your own mechanism to call the BCCTools REST services.  
2. Utilize the bcctools python wrappers directly. These are located in common-python/bcctools/bcc_rest.  
3. Utilize the bcctools Ansible modules provided. Sample playbooks are included. These are located in common-python/bcctools.  

## Security
All BCC REST services require a valid session confirmation number (_dynSessConf), and a properly authenticated user for the session being used.  
You can disable security restrictions for development purposes. Refer to the Oracle ATG Commerce product manuals, web services guide for more information on setting the enforceSessionConfirmation parameter, and removing login requirements.  

The required chain of events with security enabled is:  
1. Get a session confirmation number, and associated JSESSION ID.  
2. Authenticate/login a user using this session confirmation number and associated JSESSION ID.  
3. You can now make calls to the other REST services. You must use this authenticated session confirmation number and associated JSESSION ID for subsequent REST calls.  


# Provided REST services
The REST services provided by the BCCTools module are defined in the ActorChainRestRegistry.properties file.

/com/oracle/ateam/bcctools/BCCActor/addTarget
 
# CURL examples  
The following are a few curl examples of interacting with the REST services. 

## Get a session confirmation number and JSESSIONID
Request:  
curl -L -v -c cookies.txt -H "Content-Type: application/json" "http://localhost:7103/rest/model/atg/rest/SessionConfirmationActor/getSessionConfirmationNumber"

Example Response:  
{"sessionConfirmationNumber":-6957835531229764888}

This call gets a new session confirmation number and JSESSIONID. The JSESSIONID is stored in cookies.txt. The sessionConfirmationNumber is returned from the REST call. You need both of these values for all subsequent REST calls.  

## Authenticate a user
Request:  
curl -L -v -b cookies.txt -H "Content-Type: application/json" \
-d "{\"login\":\"admin\", \"password\":\"admin123\", \"_dynSessConf\":\"-6957835531229764888\"}" "http://localhost:7103/rest/model/atg/userprofiling/InternalProfileActor/login"

Example Response:  
{"userId":"portal-admin"}

This call uses the cookies.txt you created with the getSessionConfirmationNumber call, and the session confirmation number returned by that call.  
It attempts to authenticate user admin with password admin123.  
If the login is successul, you will see a response similar to the example provided. This response shows the userId that corresponds to the username/password you authenticated with.  

## Return all topologies
Request:  
curl -L -v -b cookies.txt -H "Content-Type: application/json" -d "{\"_dynSessConf\":\"-6957835531229764888\"}" "http://localhost:7103/rest/model/com/oracle/ateam/bcctools/BCCActor/getAllTopologies"

Example Response:
{"topologies":[{"ID":"200001",.....
The output will be large if you have defined topologies.

This call uses the cookies.txt you created with the getSessionConfirmationNumber call, and the session confirmation number returned by that call.
The JSESSIONID in your cookies.txt should now have an authenticated status from your login call.  
If you are not properly authenticated, you will get an error message returned.

### 409 errors
If you receive 409 errors, that indicates the _dynSessConf value you are using is not valid, or not a correct match for your JSESSIONID.  

# Additional API info
See
[REST-APIs](https://github.com/oracle/atg-commerce-iaas/blob/master/BCCTools/REST-APIs.md)
for details on each REST service.

  
