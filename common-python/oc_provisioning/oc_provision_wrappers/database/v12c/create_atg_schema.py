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

import fileinput
import platform
import os
import logging

import cx_Oracle

logger = logging.getLogger(__name__)

json_key = 'CIMConfig'
service_name = "Oracle DBaaS"

def alter_pub_table(configData,full_path):
   logger.info("Altering the pub table.....")

   if json_key in configData:
        jsonData = configData[json_key]
   else:
        logging.error(json_key + " config data missing from json. will not create the ATG schema")
        return

   logger.info("creating schema....")

   requiredFields = ['DB_HOST', 'PLUG_DBNAME', 'DB_PORT', 'ATG_PUBLISHING_USER', 'ATG_PUBLISHING_PASSWORD']

   commerce_setup_helper.check_required_fields(jsonData, requiredFields)

   DBHOST = jsonData['DB_HOST']
   PLUGDBNAME = jsonData['PLUG_DBNAME']
   DBPORT = jsonData['DB_PORT']
   PUBUSR = jsonData['ATG_PUBLISHING_USER']
   PUBPASSWD = jsonData['ATG_PUBLISHING_PASSWORD']

   oracle_replacements = {'DB_HOST':DBHOST, 'PLUG_DBNAME':PLUGDBNAME,'DB_PORT':DBPORT, 'ATG_PUBLISHING_USER':PUBUSR,'ATG_PUBLISHING_PASSWORD':PUBPASSWD}


   con = cx_Oracle.connect(PUBUSR, PUBPASSWD, DBHOST + ':' + DBPORT + '/' + PLUGDBNAME)

   cur = con.cursor()

   try:
       cur.execute("ALTER TABLE epub_deployment MODIFY (URI VARCHAR2(200))")
   except TypeError as e:
      logger.info("Error altering pub table .....")

      logging.error("Error with altering table: " + e)

   cur.close()

   con.commit()

   con.close()

   logger.info("Connected to the pdb in DBaaS and altered the pub table...")



def schema_definition(configData, full_path):
   logger.info("start creating the ATG schema....")

   if json_key in configData:
        jsonData = configData[json_key]
   else:
        logging.error(json_key + " config data missing from json. will not create the ATG schema")
        return

   logger.info("creating schema....")

   #required fields

   requiredFields = ['DB_HOST', 'PLUG_DBNAME', 'DB_PORT', 'ATG_TABLESPACE','SYSTEM_PASSWD','ATG_SWITCH_A_USER','ATG_SWITCH_B_USER','ATG_PUBLISHING_USER','ATG_PROD_USER','ATG_SWITCH_A_PASSWORD','ATG_SWITCH_B_PASSWORD','ATG_PUBLISHING_PASSWORD','ATG_PROD_PASSWORD']

   commerce_setup_helper.check_required_fields(jsonData, requiredFields)

   DBHOST = jsonData['DB_HOST'] 
   PLUGDBNAME = jsonData['PLUG_DBNAME'] 
   DBPORT = jsonData['DB_PORT'] 
   ATGTABLESPACE = jsonData['ATG_TABLESPACE']
   SYSPASSWD = jsonData['SYSTEM_PASSWD']
   SWITCHAUSR = jsonData['ATG_SWITCH_A_USER']
   SWITCHBUSR = jsonData['ATG_SWITCH_B_USER']
   PUBUSR = jsonData['ATG_PUBLISHING_USER']
   PRODUSR = jsonData['ATG_PROD_USER']
   SWITCHAPASSWD = jsonData['ATG_SWITCH_A_PASSWORD']
   SWITCHBPASSWD = jsonData['ATG_SWITCH_B_PASSWORD']
   PUBPASSWD = jsonData['ATG_PUBLISHING_PASSWORD']
   PRODPASSWD = jsonData['ATG_PROD_PASSWORD']

   oracle_replacements = {'DB_HOST':DBHOST, 'PLUG_DBNAME':PLUGDBNAME,'DB_PORT':DBPORT,'ATG_TABLESPACE':ATGTABLESPACE, 'SYSTEM_PASSWD':SYSPASSWD,'ATG_SWITCH_A_USER':SWITCHAUSR, 'ATG_SWITCH_B_USER':SWITCHBUSR, 'ATG_PUBLISHING_USER':PUBUSR, 'ATG_PROD_USER':PRODUSR, 'ATG_SWITCH_A_PASSWORD':SWITCHAPASSWD, 'ATG_SWITCH_B_PASSWORD':SWITCHBPASSWD, 'ATG_PUBLISHING_PASSWORD':PUBPASSWD, 'ATG_PROD_PASSWORD':PRODPASSWD}


   con = cx_Oracle.connect('system', SYSPASSWD, DBHOST + ':' + DBPORT + '/' + PLUGDBNAME)

   logger.info("con version: " + con.version)

   cur = con.cursor()

   cur.execute("SELECT 'Hello world!' FROM dual")

   createTableSpaceCommand = "\"create bigfile tablespace " + ATGTABLESPACE + " DATAFILE SIZE 1G autoextend on next 1G maxsize 20G \""
   logger.info("This is the createTableSpaceCommand : " + createTableSpaceCommand)

   dropSwitchACommand = "\"drop usere " + SWITCHAUSR + " cascade\""
   logger.info("This is the dropSwitchACommand : " + dropSwitchACommand)

   dropSwitchBCommand = "\"drop user " + SWITCHBUSR + " cascade\""
   logger.info("This is the dropSwitchBCommand : " + dropSwitchBCommand)

   dropPubCommand = "\"drop user " + PUBUSR + " cascade\""
   logger.info("This is the dropPubCommand : " + dropPubCommand)

   dropProdCommand = "\"drop user " + PRODUSR + " cascade\""
   logger.info("This is the dropProdCommand : " + dropProdCommand)
   
   createSwitchACommand = "\"create user " + SWITCHAUSR + " identified by " + SWITCHAPASSWD + " default tablespace " +  ATGTABLESPACE + "\""
   logger.info("This is the createSwitchACommand : " + createSwitchACommand)

   createSwitchBCommand = "\"create user " + SWITCHBUSR + " identified by " + SWITCHBPASSWD + " default tablespace " +  ATGTABLESPACE + "\""
   logger.info("This is the createSwitchBCommand : " + createSwitchBCommand)

   createPubCommand = "\"create user " + PUBUSR + " identified by " + PUBPASSWD + " default tablespace " +  ATGTABLESPACE + "\""
   logger.info("This is the createPubCommand : " + createPubCommand)

   createProdCommand = "\"create user " + PRODUSR + " identified by " + PRODPASSWD + " default tablespace " +  ATGTABLESPACE + "\""
   logger.info("This is the createProdCommand : " + createProdCommand)

   grantSwitchACommand = "\"grant connect,resource,dba to " + SWITCHAUSR + "\""
   logger.info("This is the grantSwitchACommand : " + grantSwitchACommand)

   grantSwitchBCommand = "\"grant connect,resource,dba to " + SWITCHBUSR + "\""
   logger.info("This is the grantSwitchBCommand : " + grantSwitchBCommand)

   grantPubCommand = "\"grant connect,resource,dba to " + PUBUSR + "\""
   logger.info("This is the grantPubCommand : " + grantPubCommand)

   grantProdCommand = "\"grant connect,resource,dba to " + PRODUSR + "\""
   logger.info("This is the grantProdCommand : " + grantProdCommand)

   cur.close()

   con.commit()
              
   con.close()

   #print("Connecting to the pdb in DBaaS....")
   logger.info("Connected to the pdb in DBaaS...")
