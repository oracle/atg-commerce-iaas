#!/bin/bash

if [ .${ORACLE_SYSTEM_USERNAME} == . ]; then
    ORACLE_SYSTEM_USERNAME=system
fi

if [ .${ORACLE_SYSTEM_PASSWORD} == . ]; then
    ORACLE_SYSTEM_PASSWORD=Password123#
fi

if [ .${ORACLE_SID} == . ]; then
    ORACLE_SID=orcl
fi


echo -e "\n" \
        "\n====================================================================================================" \
        "\n=== Creating the schemas for Oracle SID ${ORACLE_SID}" \
        "\n====================================================================================================\n"
read -p "Press enter to continue"

sqlplus ${ORACLE_SYSTEM_USERNAME}/${ORACLE_SYSTEM_PASSWORD}@${ORACLE_SID} <<EOF
-- =============================================================================
--   Create the ATG users/schemas.
-- =============================================================================
CREATE USER atgcore IDENTIFIED BY Password123 DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE temp;
CREATE USER atgcata IDENTIFIED BY Password123 DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE temp;
CREATE USER atgcatb IDENTIFIED BY Password123 DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE temp;
CREATE USER atgca   IDENTIFIED BY Password123   DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE temp;
CREATE USER atgstg   IDENTIFIED BY Password123   DEFAULT TABLESPACE USERS TEMPORARY TABLESPACE temp;

grant dba to atgca;
grant dba to atgcore;
grant dba to atgcata;
grant dba to atgcatb;
grant dba to atgstg;

exit
EOF
