import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2_resource = boto3.resource('ec2', 'us-east-1')

    ## START-STOP EC2 instances with the Schedule tag equal to 'office-hours' ##

    instances = ec2_resource.instances.filter(
        Filters=[
                  {'Name': 'tag:Schedule', 'Values': ['office-hours']},
       ]
    )

    for instance in instances:
       instance_name = ''
       for tag in instance.tags:
          if tag['Key'] == 'Name':
             instance_name = tag['Value']
       if instance.state['Name'] == 'running':
          print(instance_name + ' is currently running but it will be stopped')
          instance.stop()
       if instance.state['Name'] == 'stopped':
          print(instance_name + ' is currently stopped but it will be started')
          instance.start()
