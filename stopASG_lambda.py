import os
import boto3
from datetime import datetime

print("Lambda_trigerred at ", datetime.now())
client = boto3.client('autoscaling')

dynamodb = boto3.resource('dynamodb')

def write_data_in_database(params):
    print('Writing DynamoDb')
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table("autoscheduler-table")
        table.put_item(Item=params)
    except Exception as e:
        print(f"DynamoDb Exception {e}!")
        return False
    print("Data add successfully.")
    return True


def lambda_handler(event, context):
    
    # paginator = client.get_paginator('describe_auto_scaling_groups')
    # page_iterator = paginator.paginate(PaginationConfig={'PageSize': 100})
    # filtered_asgs = page_iterator.search('AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format('', ''))
    # print(filtered_asgs)
    autoscalinggroups = client.describe_auto_scaling_groups()['AutoScalingGroups']
    for asg in autoscalinggroups:
        print(asg['AutoScalingGroupName'])
        params = {
            'ASG_name' : asg['AutoScalingGroupName'],
            'LastShutDownAt' : str(datetime.now()),
            'MinSize' : asg['MinSize'],
            'MaxSize' : asg['MaxSize'],
            'DesiredCapacity' : asg['DesiredCapacity']
        }
        print(params)
        write_data_in_database(params)
        response = client.update_auto_scaling_group(
            AutoScalingGroupName=asg['AutoScalingGroupName'],
            MinSize=0,
            MaxSize=0,
            DesiredCapacity=0,
        )
