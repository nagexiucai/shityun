#!/usr/bin/env sh

# TODO: inotifywait|me, monitor ouput of inotifywait in me then perform rsync once

echo "please input ip."

read REGISTRY

echo "u typed $REGISTRY."

#read DEBUG
#if [ $DEBUG = "exit" ]
#then
#exit
#fi

while true
do
    echo "start sync..." `date`
    # rsync -av rsync-user@$REGISTRY::module /path-to-module --password-file=/etc/rsync.secrets # run at slave
    rsync -av /path-to-module rsync-user@$REGISTRY::module --password-file=/etc/rsync.secrets
done
