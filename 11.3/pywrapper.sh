#!/bin/sh

# Check for root
if [ `id -u` != 0 ]; then
    echo "you must be root to use this script"
    exit 4
fi

/opt/oracle/install/11.3/commerce_setup.py $@ >> /opt/oracle/install/11.3/opc-installer.log 2>&1

