#Lambda Script to take Snapshots of specific Instances

import boto3
from datetime import datetime, timedelta


def lambda_handler(event, context):
    ec2_resource = boto3.resource('ec2', 'us-east-1')

    ## TAKE SNAPSHOTS ##

    # Get a list of all the running instances
    instances = ec2_resource.instances.filter(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']},
            {'Name': 'tag:Backup', 'Values': ['yes']}
        ]
    )

    for instance in instances:
        instance_name = ''
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                instance_name = tag['Value']

        print(instance.id, instance_name, instance.block_device_mappings[0]['Ebs']['VolumeId'], instance.instance_type)

        # Take snapshots of the volume
        for volume in instance.block_device_mappings:
            volume_id = volume['Ebs']['VolumeId']
            snapshot = ec2_resource.create_snapshot(
                Description=instance_name + '-Snapshot. Created by backup script',
                VolumeId=volume_id
            )
            snapshot.create_tags(Tags=[{'Key': 'backup', 'Value': 'yes'}])

    ## REMOVE OLD SNAPSHOTS  ##

    # Specify the retention time
    retention_days = 7
    delete_time = datetime.utcnow() - timedelta(retention_days)

    snapshots = ec2_resource.snapshots.filter(
        Filters=[{'Name': 'tag:backup', 'Values': ['yes']}])

    for snapshot in snapshots:
        snapshot_time = snapshot.start_time.replace(tzinfo=None)
        if (snapshot_time < delete_time):
            snapshot.delete()
