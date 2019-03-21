import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    rds_client = boto3.client('rds', 'us-east-1')

    # TAKE RDS SNAPSHOT - Instance 'rds-sqlinstance'
    rds_client.create_db_snapshot(
        DBSnapshotIdentifier='rds-sqlinstance-snapshot-script-'+datetime.now().strftime("%m-%d-%y"),
        DBInstanceIdentifier='rds-sqlinstance',
        Tags=[
            {
                'Key': 'script_backup',
                'Value': 'yes'
            },
        ]
    )

    # REMOVE OLD RDS SNAPSHOTS - Instance 'rds-sqlprod'
    rds_snapshots = rds_client.describe_db_snapshots(DBInstanceIdentifier='rds-sqlinstance')

    retention_days = 7
    delete_time = datetime.utcnow() - timedelta(retention_days)

    for snapshot in rds_snapshots['DBSnapshots']:
        # Make sure there is not any snapshot on the creating state
        if snapshot['Status'] == 'available':
            tags = rds_client.list_tags_for_resource(ResourceName=snapshot['DBSnapshotArn'])
            for tag in tags['TagList']:
                if tag['Key'] == 'script_backup' and tag['Value'] == 'yes':
                    snapshot_identifier = snapshot['DBSnapshotIdentifier']
                    snapshot_time = snapshot['SnapshotCreateTime'].replace(tzinfo=None)
                    if snapshot_time < delete_time:
rds_client.delete_db_snapshot(DBSnapshotIdentifier=snapshot_identifier)
