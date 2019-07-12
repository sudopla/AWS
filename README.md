# AWS

###Backup_To_S3

This script allows you to back up a directory to Amazon S3.

In the process, the script will create a mirror directory where each file will only contain the modification date of the original file. Doing this, the script will only copy to Amazon S3 the new files or the ones that were modified, saving a lot of bandwidth and time.

Also, the script will remove in S3 the files that were removed in the source directory.


#Start_Stop_EC2_Instances

Create two CloudWath events with the start and stop times respectively and add them as triggers to the Lambda function. 
You will also need to tag the machines that will be in this schedule with the Schedule=office-hours. 
