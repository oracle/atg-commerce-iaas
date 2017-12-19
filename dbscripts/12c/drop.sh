#!/bin/bash

if [ .${ORACLE_SYSTEM_USERNAME} == . ]; then
    ORACLE_SYSTEM_USERNAME=system
fi

if [ .${ORACLE_SYSTEM_PASSWORD} == . ]; then
    ORACLE_SYSTEM_PASSWORD=Password123
fi

if [ .${ORACLE_SID} == . ]; then
    ORACLE_SID=orcl
fi


echo -e "\n" \
        "\n====================================================================================================" \
        "\n=== Dropping the ATG schemas for Oracle SID ${ORACLE_SID}" \
        "\n====================================================================================================\n"
read -p "Press enter to continue"

sqlplus ${ORACLE_SYSTEM_USERNAME}/${ORACLE_SYSTEM_PASSWORD}@${ORACLE_SID} <<EOF
-- =============================================================================
--   Drop the ATG users/schemas.
-- =============================================================================
DROP USER c##atgcore cascade;
DROP USER c##atgcata cascade;
DROP USER c##atgcatb cascade;
DROP USER c##atgca   cascade;
DROP USER c##atgstg  cascade;

exit
EOF
