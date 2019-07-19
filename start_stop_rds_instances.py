import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    rds_client = boto3.client('rds', 'us-east-1')

    ## START-STOP RDS instances with the Schedule tag equal to 'office-hours' ##

    rds_instances = rds_client.describe_db_instances()

    for rds_instance in rds_instances['DBInstances']:
        tags = rds_client.list_tags_for_resource(ResourceName=rds_instance['DBInstanceArn'])
        for tag in tags['TagList']:
            if tag['Key'] == 'Schedule' and tag['Value'] == 'office-hours':
                instance_identifier = rds_instance['DBInstanceIdentifier']
                if rds_instance['DBInstanceStatus'] == 'available':
                    print('RDS instance - ' + instance_identifier + ' is running but it will be stopped')
                    rds_client.stop_db_instance(DBInstanceIdentifier=instance_identifier)
                elif rds_instance['DBInstanceStatus'] == 'stopped':
                    print('RDS instance - ' + instance_identifier + ' is stopped but it will be started')
                    rds_client.start_db_instance(DBInstanceIdentifier=instance_identifier)

