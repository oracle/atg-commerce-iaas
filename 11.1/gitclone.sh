#!/bin/sh

// get the latest scripts
git clone --depth=1 $@ /tmp/gitclone
cp -R /tmp/gitclone/* /opt/oracle/install/11.1
rm -rf /tmp/gitclone
