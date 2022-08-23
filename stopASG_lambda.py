import os
import boto3
from datetime import datetime

print("Lambda_trigerred at ", datetime.now())


dynamodb = boto3.resource('dynamodb')



def lambda_handler(event, context):
    for region in os.environ["REGIONS"].split(","):
        asg_client = boto3.client('autoscaling',region_name=region)
        ASGscaleDown(asg_client,region)
        ec2 = boto3.resource('ec2',region_name=region)
        Ec2ScaleDown(ec2,region)
        
def ASGscaleDown(client,region):
    label = str(os.environ['ASG_LABEL']).split(":")
    
    paginator = client.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate(
        PaginationConfig={'PageSize': 100}
    )
    if label!="all":
        key = "tag:"+label[0]
        value = []
        value.append(label[1])
        filters=[
                {'Name': key,'Values': value}
            ]
        autoscalinggroups = client.describe_auto_scaling_groups(Filters=filters)['AutoScalingGroups']
    else:
        autoscalinggroups = client.describe_auto_scaling_groups()['AutoScalingGroups']
        
    for asg in autoscalinggroups:
        print(asg['AutoScalingGroupName'])
        params = {
            'Name' : asg['AutoScalingGroupName'],
            'LastShutDownAt' : str(datetime.now()),
            'MinSize' : asg['MinSize'],
            'MaxSize' : asg['MaxSize'],
            'DesiredCapacity' : asg['DesiredCapacity'],
            'Region' : region,
            'Type' : "ASG"
        }
        print(params)
        
        write_data_in_database(params)
        response = client.update_auto_scaling_group(
            AutoScalingGroupName=asg['AutoScalingGroupName'],
            MinSize=0,
            MaxSize=0,
            DesiredCapacity=0,
        )
        
def Ec2ScaleDown(ec2,client,region):
    label = str(os.environ['EC2_LABEL']).split(":")
    if label!="all":
        key = "tag:"+label[0]
        value = []
        value.append(label[1])
        filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': key,            'Values': value}
            ]
    else:
        filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
            ]
    instances = ec2.instances.filter(Filters=filters)
    instances.stop()
    
def write_data_in_database(params):
    print('Writing DynamoDb')
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ["TABLE_NAME"])
        table.put_item(Item=params)
    except Exception as e:
        print(f"DynamoDb Exception {e}!")
        return False
    print("Data add successfully.")
    return True