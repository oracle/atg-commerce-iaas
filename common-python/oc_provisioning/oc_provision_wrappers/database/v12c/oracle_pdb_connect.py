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
#con = cx_Oracle.connect('TEST', 'WelcomeA##11', 'atg113db.sub07240245012.ocnetwork.oraclevcn.com:1521/atgpdb.sub07240245012.ocnetwork.oraclevcn.com')

con = cx_Oracle.connect('system', 'AutoT1_1111669#', 'dbautotest1.autosubnetest3.autovcntest1.oraclevcn.com:1521/AT1PDB.autosubnetest3.autovcntest1.oraclevcn.com')
  
print con.version

cur = con.cursor()

cur.execute("SELECT 'Hello world!' FROM dual")

#SQL = "create tablespace ATGAUTOMATE DATAFILE SIZE 500M autoextend on next 100m maxsize 10G"

"""
try:
   cur.execute("drop user SWITCH_B cascade")
   cur.execute("drop user SWITCH_A cascade")
   cur.execute("drop user CORE cascade")
   cur.execute("drop user PUBLISHING cascade")
except:
   "users don't exist...."
   pass


try:
   cur.execute("create user SWITCH_A identified by AtgT_01111# default tablespace ATGAUTOMATE")
   cur.execute("create user SWITCH_B identified by AtgT_01111# default tablespace ATGAUTOMATE")
   cur.execute("create user CORE identified by AtgT_01111# default tablespace ATGAUTOMATE")
   cur.execute("create user PUBLISHING identified by AtgT_01111# default tablespace ATGAUTOMATE")
except TypeError as e:
   print "Error creating users...."
   print(e)


try:
   cur.execute("grant connect,resource,dba to SWITCH_A")
   cur.execute("grant connect,resource,dba to SWITCH_B")
   cur.execute("grant connect,resource,dba to CORE")
   cur.execute("grant connect,resource,dba to PUBLISHING")
except TypeError as e:
   print "Error grating permissions to users...."
   print(e)

"""

#cur.execute(SQL)

cur.execute('select username from dba_users where username = \'TEST\'')
for result in cur:
    print result

cur.close()

con.commit()
              
con.close()

print("Connecting to the pdb in DBaaS....")
