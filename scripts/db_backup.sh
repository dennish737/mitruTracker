#!/bin/bash
# Shell script to backup MySql database
# To backup Mysql databases file to /backup dir and later pick up by your
# script. You can skip few databases from backup too.

# Last updated: November 2023
# --------------------------------------------------------------------
# This is a free shell script under GNU GPL version 2.0 or above
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Backup storage directory
backupfolder=/var/backups

# MySQL user
user=<user_name>
# MySQL password
# Read mysql user password:
echo -n "Type mysql $user password: "
read -s password
echo ""

sqlfile=$backupfolder/all-database-$(date +%d-%m-%Y_%H-%M-%S).sql
zipfile=$backupfolder/all-database-$(date +%d-%m-%Y_%H-%M-%S).zip
# Create a backup
sudo mysqldump -u $user -p$password --all-databases > $sqlfile
if [ $? == 0 ]; then
  echo 'Sql dump created'
else
  echo 'mysqldump return non-zero code'
  exit
fi
# Compress backup
zip $zipfile $sqlfile
if [ $? == 0 ]; then
  echo 'The backup was successfully compressed'
else
  echo 'Error compressing backup'
  exit
fi
rm $sqlfile
