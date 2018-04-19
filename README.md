# AWS

###Backup_To_S3

This script allows you to back up a directory to Amazon S3.

In the process, the script will create a mirror directory where each file will only contain the modification date of the original file. Doing this, the script will only copy to Amazon S3 the new files or the ones that were modified, saving a lot of bandwidth and time.

Also, the script will remove in S3 the files that were removed in the source directory.
