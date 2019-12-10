**Back up files to S3**

The script [backup_to_S3.py](backup_to_S3.py) allows you to back up a directory to Amazon S3.

In the process, the script will create a mirror directory where each file will only contain the modification date of the original file. Doing this, the script will only copy to Amazon S3 the new files or the ones that were modified, saving a lot of bandwidth and time.

Also, the script will remove in S3 the files that were removed in the source directory.

**Back up EC2 instances**

The Lambda funtion [take_snapshots.py](take_snapshots.py) backs up the volumes attached to running EC2 instances tagged with Backup=yes. </br>
This function will also remove snapshots older than the specified retention time. 

IAM role for this function
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot",
                "ec2:CreateTags",
                "ec2:ModifySnapshotAttribute",
                "ec2:ResetSnapshotAttribute"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

**Run EC2 and RDS instances on a recurring schedule**

The Lambda functions [start_stop_ec2_instances.py](start_stop_ec2_instances.py) and [start_stop_rds_instances.py](start_stop_rds_instances.py) allow to to run EC2 or RDS instances only during a daily schedule. </br>
Create two CloudWatch events with the start and stop times respectively and add them as triggers to the Lambda functions. 
You will also need to tag the machines or RDS instnaces that will be in this schedule with Schedule=office-hours. 

IAM role for start_stop_ec2_instances.py function. Please notice that in this example the EBS volumes are encrypted so you have to allow the function to access the KMS key. 
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Start*",
                "ec2:Stop*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*",
                "kms:DescribeKey",
                "kms:CreateGrant",
                "kms:ListGrants",
                "kms:RevokeGrant"
            ],
            "Resource": "arn:aws:kms:us-east-1:899161478222:key/532z11f1-8530-99a2-b573-118988d0020f"
        }
    ]
}
```
IAM role for start_stop_rds_instances.py function. Please notice that in this example the RDS instances are encrypted so you have to allow the function to access the KMS key. 
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "rds:DescribeDBInstances",
                "rds:StopDBInstance",
                "rds:StartDBInstance",
                "rds:ListTagsForResource"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:ReEncrypt*",
                "kms:GenerateDataKey*",
                "kms:DescribeKey",
                "kms:CreateGrant",
                "kms:ListGrants",
                "kms:RevokeGrant"
            ],
            "Resource": "arn:aws:kms:us-east-1:899161478222:key/532z11f1-8530-99a2-b573-118988d0020f"
        }
    ]
}
```
