#!/bin/sh

cd /opt/oracle/install
sudo -u oracle git fetch --all
sudo -u oracle git reset --hard origin/master

