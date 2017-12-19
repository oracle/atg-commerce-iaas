#!/bin/bash

if [ .${ORACLE_SYSTEM_USERNAME} == . ]; then
    ORACLE_SYSTEM_USERNAME=system
fi

if [ .${ORACLE_SYSTEM_PASSWORD} == . ]; then
    ORACLE_SYSTEM_PASSWORD=password1
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
CREATE USER c##atgcore IDENTIFIED BY Password123 DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp;
CREATE USER c##atgcata IDENTIFIED BY Password123 DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp;
CREATE USER c##atgcatb IDENTIFIED BY Password123 DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp;
CREATE USER c##atgca   IDENTIFIED BY Password123   DEFAULT TABLESPACE users   TEMPORARY TABLESPACE temp;
CREATE USER c##atgstg  IDENTIFIED BY Password123 DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp;

-- =============================================================================
--   Grant DBA privledges to the ATG users (development only).
-- =============================================================================
GRANT DBA TO c##atgcore;
GRANT DBA TO c##atgcata;
GRANT DBA TO c##atgcatb;
GRANT DBA TO c##atgca;
GRANT DBA TO c##atgstg;

exit
EOF

