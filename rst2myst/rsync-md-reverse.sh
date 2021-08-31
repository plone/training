#!/bin/sh
# rsync-training.sh
#
# Use this script after building and comparing reST and MyST docs.
#
# It synchronizes all documentation files back to the original training
# directory from the rsync-training directory.
#
# To run this script, change directory to the script, then issue the following
# command:
#
# ./rsync-md-reverse.sh
#
# A detailed activity log is appended to ./rsync-md-reverse.log.
#
# NOTE: To escape spaces in directory names, you need to use double-quotes
# around the rsync command argument variable.
#
# Common options from https://download.samba.org/pub/rsync/rsync.html
#
#      --delete                delete extraneous files from dest dirs
#      --force                 force deletion of dirs even if not empty
#  -g, --group                 preserve group
#  -o, --owner                 preserve owner (super-user only)
#  -p, --perms                 preserve permissions
#  -r, --recursive             recurse into directories
#  -t, --times                 preserve modification times
#  -v, --verbose               increase verbosity
#  -z, --compress              compress file data during the transfer
#  -C, --cvs-exclude           auto-ignore files in the same way CVS does
#  -O, --omit-dir-times        omit directories from --times

cwd=".."
date=`date "+DATE: %Y-%m-%d %H:%M:%S"`

# Move *.md only and delete source
optsmd="-gioprtvzCO \
    --include-from=$cwd/rst2myst/rsync-training-md-include.txt \
    --exclude-from=$cwd/rst2myst/rsync-training-md-exclude.txt \
    --delete --force --remove-source-files"

# set the log file
log="$cwd/rst2myst/rsync-md-reverse.log"

# set source and destination
src="$cwd/rst2myst/training/"
dest="$cwd"

echo "#### $date ####" >> $log
echo "" >> $log

echo "--- Move *.md only and delete source ---" >> $log
echo "rsync $optsmd $src $dest >> $log 2>&1" >> $log
rsync $optsmd $src $dest >> $log 2>&1
echo "" >> $log
echo "" >> $log
echo "" >> $log
