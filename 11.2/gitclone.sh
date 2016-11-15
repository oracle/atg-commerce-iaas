#!/bin/sh

// get the latest scripts
git clone --depth=1 oracle@129.144.54.49:/opt/oracle/git/project.git /tmp/gitclone
cp -R /tmp/gitclone/* /opt/oracle/gittest
rm -rf /tmp/gitclone
