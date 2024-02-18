#!/bin/bash
# Shell script to backup MySql database
# To backup Mysql databases file to /backup dir and later pick up by your
# script. You can skip few databases from backup too.

# Last updated: November 2023
# --------------------------------------------------------------------
# This is a free shell script under GNU GPL version 2.0 or above
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------

MyUSER=""                   # USERNAME
MyPASS=""                   # PASSWORD
MyHOST="localhost"          # Hostname

# Linux bin paths, change this if it can not be autodetected via which command
MYSQL="$(which mysql)"
MYSQLDUMP="$(which mysqldump)"
CHOWN="$(which chown)"
CHMOD="$(which chmod)"
GZIP="$(which gzip)"

# Backup Dest directory, change this if you have someother location
DEST="/backup"

# Main directory where backup will be stored
MBD="$DEST/mysql"

# Get hostname
HOST="$(hostname)"

# Get data in dd-mm-yyyy format
NOW="$(date +"%d-%m-%Y")"

# File to store current backup file
FILE=""
# Store list of databases
DBS=""

# DO NOT BACKUP these databases
IGGY="test information_schema"

[ ! -d $MBD ] && mkdir -p $MBD || :

# Only root can access it!
$CHOWN root:root -R $DEST
$CHMOD 0600 $DEST

# Get all database list first
DBS="$($MYSQL -u $MyUSER -h $MyHOST -p$MyPASS -Bse 'show databases')"

for db in $DBS
do
    skipdb=-1
    if [ "$IGGY" != "" ];
    then
        for i in $IGGY
        do
            [ "$db" == "$i" ] && skipdb=1 || :
        done
    fi

    if [ "$skipdb" == "-1" ] ; then
        FILE="$MBD/$db.$HOST.$NOW.gz"
        # do all inone job in pipe,
        # connect to mysql using mysqldump for select mysql database
        # and pipe it out to gz file in backup dir :)
        $MYSQLDUMP -u $MyUSER -h $MyHOST -p$MyPASS $db | $GZIP --rsyncable -9 > $FILE
    fi
done