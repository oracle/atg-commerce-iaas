# The MIT License (MIT)
#
# Copyright (c) 2018 Oracle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = "Hadi Javaheriani (Oracle IaaS and App Dev Team)"
__copyright__ = "Copyright (c) 2018  Oracle and/or its affiliates. All rights reserved."
__version__ = "1.0.0.1"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


from oc_provision_wrappers import commerce_setup_helper
import os
import platform
import logging
#from array import * 

logger = logging.getLogger(__name__)

common_key = 'WEBLOGIC_common'

atg_key = 'ATG_install'
#json_dynamo_key = 'dynamoRoot'

json_cim_key = 'CIMConfig'
json_key = 'WEBLOGIC_machines'
service_name = "CIM"
CONFIG_CIM = True

#keep these instance names gobal
SSOAPP = None
PRODAPP = None
PUBAPP = None
SLMAPP = None

instances = []

INSTALL_DIR = None
INSTALL_OWNER = None
INSTALL_GROUP = None
WL_DOMAIN_HOME = None
ADMIN_URL = None

#We are copying a few tag libs that are mismatched in DAS and CRS
def pre_cim_setup(configData, full_path):
    if atg_key in configData:
        jsonData = configData[atg_key]
    else:
        logging.error(atg_key + " config data missing from json. will not continue....")
        return False

    logging.info("making config changes before CIM runs" )

    DAS_tag = "cp " + jsonData + "/DAS/taglib/dspjspTaglib/1.0/lib/dspjspTaglib1_0.jar"

    fluoroscope_tag = jsonData + "/CommerceReferenceStore/Store/Fluoroscope/j2ee-apps/Fluoroscope/fluoroscope.war/WEB-INF/lib/"
    merchandising_tag = jsonData + "/CommerceReferenceStore/Store/EStore/Versioned/j2ee-apps/Versioned/store-merchandising.war/WEB-INF/lib/"
    store_tag = jsonData + "/CommerceReferenceStore/Store/Storefront/j2ee-apps/Storefront/store.war/WEB-INF/lib/"

    commerce_setup_helper.exec_cmd(DAS_tag + " " + fluoroscope_tag)
    commerce_setup_helper.exec_cmd(DAS_tag + " " + merchandising_tag)
    commerce_setup_helper.exec_cmd(DAS_tag + " " + store_tag)

def post_cim_setup(configData, full_path):
    if json_key in configData:
        jsonData = configData[json_key]
    else:
        logging.error(json_key + " config data missing from json. will not continue....")
        return False

    logging.info("Adding Managed Serves to the default machine." )

    global SSOAPP
    global PRODAPP
    global PUBAPP
    global SLMAPP

    global instances

    global INSTALL_DIR
    global INSTALL_OWNER
    global INSTALL_GROUP 
    global WL_DOMAIN_HOME
    
    logging.info("Instance bcc:  " + PUBAPP)
    logging.info("Instance sso:  " + SSOAPP)
    logging.info("Instance crs:  " + PRODAPP)
    logging.info("Instance slm:  " + SLMAPP)

    logging.info("getting the machine name and address....." )
    
    default_machine_array = commerce_setup_helper.find_default_machine(configData, full_path)

    logging.info("Just got the machine name and address....." )

    for jsonData_machine in default_machine_array:
        requiredFields = ['machineName', 'machineAddress']
        commerce_setup_helper.check_required_fields(jsonData_machine, requiredFields)

        WL_MACHINE_NAME = jsonData_machine['machineName']
        WL_MACHINE_ADDR = jsonData_machine['machineAddress']

    if common_key in configData:
        commonData = configData[common_key]
    else:
        logging.error(common_key + " config data missing from json. will not add machine")
        return 

    response_files_path = full_path + "/responseFiles/wls-12.2.1"

    commonRequiredFields = ['middlewareHome', 'installOwner', 'installGroup', 'wl_adminUser', 'wl_adminHttpPort', 'wl_adminHost', 'wl_adminPassword']
    commerce_setup_helper.check_required_fields(commonData, commonRequiredFields)

    INSTALL_DIR = commonData['middlewareHome']
    INSTALL_OWNER = commonData['installOwner']
    INSTALL_GROUP = commonData['installGroup']
    WL_ADMIN_USER = commonData['wl_adminUser']
    WL_ADMIN_PW = commonData['wl_adminPassword']
    WL_ADMIN_HOST = commonData['wl_adminHost']
    WL_ADMIN_HTTP_PORT = commonData['wl_adminHttpPort']


    """
    wlst_path = INSTALL_DIR + "/oracle_common/common/bin/wlst.sh"
    
    if not os.path.exists(wlst_path):
        logging.error("Binary " + wlst_path + " does not exist - will not install")
        return False


    logging.info("Now calling the addManagedServerToMachine ....." )

    wlCmd = "\"" + wlst_path + " " + response_files_path + "/addManagedServerToMachine.py -u " + WL_ADMIN_USER + \
        " -p " + WL_ADMIN_PW + " -a t3://" + WL_ADMIN_HOST + ":" + WL_ADMIN_HTTP_PORT + " -n " + SLMAPP + " -m " + WL_MACHINE_NAME + " -l " + WL_MACHINE_ADDR + "\""
        
    commerce_setup_helper.exec_as_user(INSTALL_OWNER, wlCmd) 
    logging.info("just called the addManagedServerToMachine.....Added instance: " + SLMAPP)


    wlCmd = "\"" + wlst_path + " " + response_files_path + "/addManagedServerToMachine.py -u " + WL_ADMIN_USER + \
        " -p " + WL_ADMIN_PW + " -a t3://" + WL_ADMIN_HOST + ":" + WL_ADMIN_HTTP_PORT + " -n " + SSOAPP + " -m " + WL_MACHINE_NAME + " -l " + WL_MACHINE_ADDR + "\""

    commerce_setup_helper.exec_as_user(INSTALL_OWNER, wlCmd)
    logging.info("just Added instance: " + SSOAPP )

    wlCmd = "\"" + wlst_path + " " + response_files_path + "/addManagedServerToMachine.py -u " + WL_ADMIN_USER + \
        " -p " + WL_ADMIN_PW + " -a t3://" + WL_ADMIN_HOST + ":" + WL_ADMIN_HTTP_PORT + " -n " + PRODAPP + " -m " + WL_MACHINE_NAME + " -l " + WL_MACHINE_ADDR + "\""

    commerce_setup_helper.exec_as_user(INSTALL_OWNER, wlCmd)
    logging.info("just Added instance: " + PRODAPP )

    wlCmd = "\"" + wlst_path + " " + response_files_path + "/addManagedServerToMachine.py -u " + WL_ADMIN_USER + \
        " -p " + WL_ADMIN_PW + " -a t3://" + WL_ADMIN_HOST + ":" + WL_ADMIN_HTTP_PORT + " -n " + PUBAPP + " -m " + WL_MACHINE_NAME + " -l " + WL_MACHINE_ADDR + "\""

    commerce_setup_helper.exec_as_user(INSTALL_OWNER, wlCmd)
    logging.info("just Added instance: " + PUBAPP )

    """

    create_cim_managed(full_path)


def create_cim_managed(full_path):

    #loop and create a script for each instance

    global instances

    global INSTALL_DIR
    global INSTALL_OWNER
    global INSTALL_GROUP
    global WL_DOMAIN_HOME
    global ADMIN_URL
    global platform

    if (platform.system() == 'SunOS'):
        startStopPath = "/startStopScripts/solaris/bootScripts/"
    else:
        startStopPath = "/startStopScripts/bootScripts/"
    
    logging.info('loopging thru the managed servers.......')

    for instance in instances:
        WL_SERVER_NAME = str(instance)

        SCRIPT_NAME = 'weblogicManaged-' + WL_SERVER_NAME
        logging.info('Generating startup script for server ' + WL_SERVER_NAME)


        wlScript_replacements = {'WL_DOMAIN_HOME':WL_DOMAIN_HOME, "WL_PROCESS_OWNER":INSTALL_OWNER, "INSTANCE_NAME":WL_SERVER_NAME, "ADMIN_URL":ADMIN_URL}
        
        commerce_setup_helper.copy_start_script('false', full_path + startStopPath + 'weblogicManaged.master', wlScript_replacements, SCRIPT_NAME)
                
        # make the path to the log dir, or first server start will fail with scripts
        logging.info('Generating log dir for server ' + WL_SERVER_NAME)
        SERVER_LOG_PATH = WL_DOMAIN_HOME + '/servers/' + WL_SERVER_NAME + '/logs'
        commerce_setup_helper.mkdir_with_perms(SERVER_LOG_PATH, INSTALL_OWNER, INSTALL_GROUP)
                
        # fire up the instance 
        logging.info('Starting up instance ' + WL_SERVER_NAME)
        #startCmd = "/etc/init.d/" + SCRIPT_NAME
        #commerce_setup_helper.exec_cmd(startCmd + " restart") 


    
def config_cim(configCIMData, full_path):
    
    if json_cim_key in configCIMData:
        jsonCIMData = configCIMData[json_cim_key]
    else:
        logging.error(json_cim_key + " config data missing from CIM json. will not install")
        return False

    global SSOAPP
    global PRODAPP
    global PUBAPP
    global SLMAPP
   
    global WL_DOMAIN_HOME
    global ADMIN_URL

    logging.info("configuring " + service_name)
    #binary_path = full_path + "/binaries/atg11.3"
    cim_files_path = "/home/oracle"
    #install_exec = "/linux/OCPlatform11.3.bin"
    #full_exec_path = binary_path + install_exec

    requiredFields = ['INSTALL_LOC_FMW', 'WLS_VERSION', 'WLS_DOMAIN_DIR', 'WLS_DOMAIN_NAME', 'WLS_HOST', 'WLS_LISTEN_PORT', 'WLS_LISTEN_sPORT', 'WLS_NODE_MANAGER_USER', 'WLS_NODE_MANAGER_PASSWORD', 'OC_DIR', 'ATG_DIR', 'ATG_VERSION', 'ENDECA_DIR', 'ENDECA_EAC_APP', 'EAC_APP_DEPLOY_PATH', 'EAC_PORT_NUMBER', 'CAS_HOST', 'CAS_PORT', 'EAC_HOST', 'DGRAPH_PORT', 'AUTH_DGRAPH_PRT', 'ENDECA_LOG_SERVER_PORT', 'CAS_VERSION','ENDECA_LANG','WORKBENCH_HOST','WORKBENCH_PORT','PREV_HOST','PREV_PORT','PREV_CONTEXT_ROOT','USER_SEG_HOST','USER_SEG_PORT','ORACLE_WALLET_DIR','EXPORT_ARCHIVE_DIR','AUTH_EXPORT_DIR','TOOLS_VERSION','MDEX_HOST', 'MDEX_VERSION', 'PLATFORM_VERSION', 'ATG_PUBLISHING_USER', 'ATG_PUBLISHING_PASSWORD', 'DB_PORT', 'DB_HOST', 'DB_NAME', 'PLUG_DBNAME', 'DB_DRIVER_PATH', 'ATG_PUB_JNDI', 'MERCH_PASSWD', 'ADMIN_PASSWD', 'ATG_SLM_APPS', 'ATG_SLM_PORT', 'ATG_SLM_sPORT', 'ATG_SLM_RMI', 'ATG_SLM_DRP', 'SRVR_LOCK_HOST', 'SRVR_LOCK_PORT', 'SLM_EAR', 'ATG_PUB_APPS', 'ATG_PUB_PORT', 'ATG_PUB_sPORT', 'ATG_PUB_RMI', 'ATG_PUB_DRP', 'ATG_PUB_FILE', 'ATG_PUB_SYNC', 'ATG_PUB_HOST', 'ATG_PUB_LOCK', 'PUB_EAR', 'ATG_PROD_USER', 'ATG_PROD_PASSWORD', 'ATG_SWITCH_A_USER', 'ATG_SWITCH_A_PASSWORD', 'ATG_SWITCH_B_USER', 'ATG_SWITCH_B_PASSWORD', 'ATG_PROD_JNDI', 'ATG_SWITCH_A_JNDI', 'ATG_SWITCH_B_JNDI', 'ATG_PROD_APPS', 'ATG_PROD_PORT', 'ATG_PROD_sPORT', 'ATG_PROD_RMI', 'ATG_PROD_DRP', 'ATG_PROD_FILE', 'PROD_EAR', 'ATG_SSO_APPS', 'ATG_SSO_PORT', 'ATG_SSO_sPORT', 'ATG_SSO_RMI', 'ATG_SSO_DRP', 'ATG_SSO_FILE', 'ATG_SSO_SYNC','ATG_SSO_HOST', 'SSO_EAR']
 
    commerce_setup_helper.check_required_fields(jsonCIMData, requiredFields)

    WLS_DIR = jsonCIMData['INSTALL_LOC_FMW']
    WSL_VER = jsonCIMData['WLS_VERSION']
    DOMAIN_DIR = jsonCIMData['WLS_DOMAIN_DIR']
    DOMAIN = jsonCIMData['WLS_DOMAIN_NAME']

    #use thi sia a global 
    WL_DOMAIN_HOME = DOMAIN_DIR + "/" +  DOMAIN

    WLSHOST = jsonCIMData['WLS_HOST']
    WLS_LISTENPORT = jsonCIMData['WLS_LISTEN_PORT']

    #a global variable

    ADMIN_URL = WLSHOST + ":" + WLS_LISTENPORT
    WLS_LISTENSPORT = jsonCIMData['WLS_LISTEN_sPORT']
    WLS_USER = jsonCIMData['WLS_NODE_MANAGER_USER']
    WLS_PASSWD = jsonCIMData['WLS_NODE_MANAGER_PASSWORD']
    
    OCDIR = jsonCIMData['OC_DIR']
    ATGDIR = jsonCIMData['ATG_DIR']
    ATGVER = jsonCIMData['ATG_VERSION']
    ENDECADIR= jsonCIMData['ENDECA_DIR']
    EACAPP = jsonCIMData['ENDECA_EAC_APP']
    EACDEPLOY = jsonCIMData['EAC_APP_DEPLOY_PATH']
    EACPORT = jsonCIMData['EAC_PORT_NUMBER']
    CASHOST = jsonCIMData['CAS_HOST']
    CASPORT = jsonCIMData['CAS_PORT']
    EACHOST = jsonCIMData['EAC_HOST']
    DGPORT = jsonCIMData['DGRAPH_PORT']
    AUTHDGPORT = jsonCIMData['AUTH_DGRAPH_PRT']
    ENDECALOGPORT = jsonCIMData['ENDECA_LOG_SERVER_PORT']
    CASVER = jsonCIMData['CAS_VERSION']
    ENDECALANG = jsonCIMData['ENDECA_LANG']
    WBENCHHOST = jsonCIMData['WORKBENCH_HOST']
    WBENCHPORT = jsonCIMData['WORKBENCH_PORT']
    PREVHOST = jsonCIMData['PREV_HOST']
    PREVPORT = jsonCIMData['PREV_PORT']
    PREVROOT = jsonCIMData['PREV_CONTEXT_ROOT']
    SEGHOST = jsonCIMData['USER_SEG_HOST']
    SEGPORT = jsonCIMData['USER_SEG_PORT']
    WALLETDIR = jsonCIMData['ORACLE_WALLET_DIR']
    EXPARCHDIR = jsonCIMData['EXPORT_ARCHIVE_DIR']
    AUTHEXPDIR = jsonCIMData['AUTH_EXPORT_DIR']
    TOOLSVER = jsonCIMData['TOOLS_VERSION']
    MDEXHOST = jsonCIMData['MDEX_HOST'] 
    MDEXVER = jsonCIMData['MDEX_VERSION'] 
    PLATVER = jsonCIMData['PLATFORM_VERSION'] 
    PUBUSR = jsonCIMData['ATG_PUBLISHING_USER'] 
    PUBPASSWD = jsonCIMData['ATG_PUBLISHING_PASSWORD'] 
    DBPORT = jsonCIMData['DB_PORT'] 
    DBHOST = jsonCIMData['DB_HOST'] 
    DBNAME = jsonCIMData['DB_NAME'] 
    PDBNAME = jsonCIMData['PLUG_DBNAME'] 
    DBDRVER = jsonCIMData['DB_DRIVER_PATH'] 
    PUBJNDI = jsonCIMData['ATG_PUB_JNDI'] 
    MERCHPASSWD = jsonCIMData['MERCH_PASSWD'] 
    ADMINPASSWD = jsonCIMData['ADMIN_PASSWD'] 
    SLMAPP = jsonCIMData['ATG_SLM_APPS'] 
    instances.append(SLMAPP)
  
    SLMPORT = jsonCIMData['ATG_SLM_PORT'] 
    SLMSPORT = jsonCIMData['ATG_SLM_sPORT'] 
    SLMRMI = jsonCIMData['ATG_SLM_RMI'] 
    SLMDRP = jsonCIMData['ATG_SLM_DRP'] 
    LOCKHOST = jsonCIMData['SRVR_LOCK_HOST'] 
    LOCKPORT = jsonCIMData['SRVR_LOCK_PORT'] 
    SLMEAR = jsonCIMData['SLM_EAR'] 
    PUBAPP = jsonCIMData['ATG_PUB_APPS'] 
    instances.append(PUBAPP)
   
    PUBPORT = jsonCIMData['ATG_PUB_PORT'] 
    PUBSPORT = jsonCIMData['ATG_PUB_sPORT'] 
    PUBRMI = jsonCIMData['ATG_PUB_RMI'] 
    PUBDRP = jsonCIMData['ATG_PUB_DRP'] 
    PUBFILE = jsonCIMData['ATG_PUB_FILE'] 
    PUBSYNC = jsonCIMData['ATG_PUB_SYNC'] 
    PUBHOST = jsonCIMData['ATG_PUB_HOST'] 
    PUBLOCK = jsonCIMData['ATG_PUB_LOCK'] 
    PUBEAR = jsonCIMData['PUB_EAR'] 
    PRODUSR = jsonCIMData['ATG_PROD_USER'] 
    PORDPASSWD = jsonCIMData['ATG_PROD_PASSWORD'] 
    SWITCHAUSR = jsonCIMData['ATG_SWITCH_A_USER'] 
    SWITCHAPASSWD = jsonCIMData['ATG_SWITCH_A_PASSWORD'] 
    SWITCHBUSR = jsonCIMData['ATG_SWITCH_B_USER'] 
    SWITCHBPASSWD = jsonCIMData['ATG_SWITCH_B_PASSWORD'] 
    PORDJNDI = jsonCIMData['ATG_PROD_JNDI'] 
    SWITCHAJNDI = jsonCIMData['ATG_SWITCH_A_JNDI'] 
    SWITCHBJNDI = jsonCIMData['ATG_SWITCH_B_JNDI'] 
    PRODAPP = jsonCIMData['ATG_PROD_APPS'] 
    instances.append(PRODAPP)
    
    PRODPORT = jsonCIMData['ATG_PROD_PORT'] 
    PRODSPORT = jsonCIMData['ATG_PROD_sPORT'] 
    PORDRMI = jsonCIMData['ATG_PROD_RMI'] 
    PRODDRP = jsonCIMData['ATG_PROD_DRP']
    PRODFILE = jsonCIMData['ATG_PROD_FILE'] 
    PRODEAR = jsonCIMData['PROD_EAR'] 
    SSOAPP = jsonCIMData['ATG_SSO_APPS'] 
    instances.append(SSOAPP)

    SSOPORT = jsonCIMData['ATG_SSO_PORT'] 
    SSOSPORT = jsonCIMData['ATG_SSO_sPORT'] 
    SSORMI = jsonCIMData['ATG_SSO_RMI'] 
    SSODRP = jsonCIMData['ATG_SSO_DRP'] 
    SSOFILE = jsonCIMData['ATG_SSO_FILE'] 
    SSOSYNC = jsonCIMData['ATG_SSO_SYNC'] 
    SSOHOST = jsonCIMData['ATG_SSO_HOST'] 
    SSOEAR= jsonCIMData['SSO_EAR'] 

    field_replacements = {'INSTALL_LOC_FMW': WLS_DIR, 'WLS_VERSION': WSL_VER,
                          'WLS_DOMAIN_DIR': DOMAIN_DIR, 'WLS_DOMAIN_NAME': DOMAIN, 'WLS_HOST': WLSHOST,
                          'WLS_LISTEN_PORT': WLS_LISTENPORT, 'WLS_LISTEN_sPORT': WLS_LISTENSPORT,
                          'WLS_NODE_MANAGER_USER': WLS_USER, 'WLS_NODE_MANAGER_PASSWORD': WLS_PASSWD, 
                          'OC_DIR': OCDIR, 'ATG_DIR': ATGDIR, 'ATG_VERSION': ATGVER, 'ENDECA_DIR': ENDECADIR, 
                          'ENDECA_EAC_APP': EACAPP, 'EAC_APP_DEPLOY_PATH': EACDEPLOY, 'EAC_PORT_NUMBER': EACPORT,
                          'CAS_HOST': CASHOST,'CAS_PORT': CASPORT, 'EAC_HOST': EACHOST, 'DGRAPH_PORT': DGPORT,
                          'AUTH_DGRAPH_PRT': AUTHDGPORT,  'ENDECA_LOG_SERVER_PORT': ENDECALOGPORT, 
                          'CAS_VERSION': CASVER, 'ENDECA_LANG': ENDECALANG, 'WORKBENCH_HOST': WBENCHHOST, 
                          'WORKBENCH_PORT': WBENCHPORT, 'PREV_HOST': PREVHOST, 'PREV_PORT': PREVPORT,
                          'PREV_CONTEXT_ROOT': PREVROOT, 'USER_SEG_HOST': SEGHOST, 'USER_SEG_PORT': SEGPORT,
                          'ORACLE_WALLET_DIR': WALLETDIR, 'EXPORT_ARCHIVE_DIR': EXPARCHDIR, 'AUTH_EXPORT_DIR': AUTHEXPDIR, 
                          'TOOLS_VERSION': TOOLSVER, 'MDEX_HOST': MDEXHOST, 'MDEX_VERSION': MDEXVER, 
                          'PLATFORM_VERSION': PLATVER, 'ATG_PUBLISHING_USER': PUBUSR,  'ATG_PUBLISHING_PASSWORD': PUBPASSWD, 
                          'DB_PORT': DBPORT, 'DB_HOST': DBHOST,'DB_NAME': DBNAME, 'PLUG_DBNAME': PDBNAME,'DB_DRIVER_PATH': DBDRVER,  
                          'ATG_PUB_JNDI': PUBJNDI, 'MERCH_PASSWD': MERCHPASSWD, 'ADMIN_PASSWD': ADMINPASSWD, 'ATG_SLM_APPS': SLMAPP,  
                          'ATG_SLM_PORT': SLMPORT,  'ATG_SLM_sPORT': SLMSPORT, 'ATG_SLM_RMI': SLMRMI, 'ATG_SLM_DRP': SLMDRP,  
                          'SRVR_LOCK_HOST': LOCKHOST,  'SRVR_LOCK_PORT': LOCKPORT,  'SLM_EAR': SLMEAR, 'ATG_PUB_APPS': PUBAPP,   
                          'ATG_PUB_PORT': PUBPORT,   'ATG_PUB_sPORT': PUBSPORT,  'ATG_PUB_RMI': PUBRMI,  'ATG_PUB_DRP': PUBDRP,  
                          'ATG_PUB_FILE': PUBFILE,  'ATG_PUB_SYNC': PUBSYNC, 'ATG_PUB_HOST': PUBHOST,  
                          'ATG_PUB_LOCK': PUBLOCK, 'PUB_EAR': PUBEAR, 'ATG_PROD_USER': PRODUSR, 'ATG_PROD_PASSWORD': PORDPASSWD,  
                          'ATG_SWITCH_A_USER': SWITCHAUSR, 'ATG_SWITCH_A_PASSWORD': SWITCHAPASSWD, 'ATG_SWITCH_B_USER': SWITCHBUSR,  
                          'ATG_SWITCH_B_PASSWORD': SWITCHBPASSWD,  'ATG_PROD_JNDI': PORDJNDI, 'ATG_SWITCH_A_JNDI': SWITCHAJNDI, 
                          'ATG_SWITCH_B_JNDI': SWITCHBJNDI,'ATG_PROD_APPS': PRODAPP, 'ATG_PROD_PORT': PRODPORT,  
                          'ATG_PROD_sPORT': PRODSPORT,  'ATG_PROD_RMI': PORDRMI, 'ATG_PROD_DRP': PRODDRP, 'ATG_PROD_FILE': PRODFILE, 'PROD_EAR': PRODEAR, 
                          'ATG_SSO_APPS': SSOAPP, 'ATG_SSO_PORT': SSOPORT, 'ATG_SSO_sPORT': SSOSPORT, 'ATG_SSO_RMI': SSORMI, 
                          'ATG_SSO_DRP': SSODRP, 'ATG_SSO_FILE': SSOFILE, 'ATG_SSO_SYNC': SSOSYNC,  'ATG_SSO_HOST': SSOHOST, 'SSO_EAR': SSOEAR }

    logger.info("The SLM instance: " + SLMAPP)
    logger.info("The BCC instance: " + PUBAPP)
    logger.info("The CRS instance: " + PRODAPP)
    logger.info("The SSO instance: " + SSOAPP)

    if (CONFIG_CIM ):
        logging.info("writing new cim file")
        commerce_setup_helper.substitute_file_fields(cim_files_path + '/atg113crsTemplate-v1.cim', cim_files_path + '/atg113crsTemplate-v1_converted.cim', field_replacements)
    else:
       logger.info("The file was NOT written.....")

        

