
**Back up files to S3**

The script [backup_to_S3.py](backup_to_S3.py) allows you to back up a directory to Amazon S3.

In the process, the script will create a mirror directory where each file will only contain the modification date of the original file. Doing this, the script will only copy to Amazon S3 the new files or the ones that were modified, saving a lot of bandwidth and time.

Also, the script will remove in S3 the files that were removed in the source directory.

**Run EC2 and RDS instances on a recurring schedule**

The Lambda functions [start_stop_ec2_instances.py](start_stop_ec2_instances.py) and [start_stop_rds_instances.py](start_stop_rds_instances.py) allow to to run EC2 or RDS instances only during a daily schedule. </br>
Create two CloudWatch events with the start and stop times respectively and add them as triggers to the Lambda functions. 
You will also need to tag the machines or RDS instnaces that will be in this schedule with Schedule=office-hours. 

**Back up EC2 instances**

The Lambda funtion [take_snapshots.py](take_snapshots.py) backs up the volumes attached to running EC2 instances tagged with Backup=yes. </br>
This function will also remove snapshots older than the specified retention time. 
