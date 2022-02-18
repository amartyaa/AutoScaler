import os
import boto3
from datetime import datetime

print("Lambda_trigerred at ", datetime.now())
client = boto3.client('autoscaling')


# below code is to read data from DynamoDB

dynamodb = boto3.resource('dynamodb')

def Read_data_in_database():
    print('Reading DynamoDb')
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table("autoscheduler-table")
        stoppedtb=table.scan()
    except Exception as e:
        print(f"DynamoDb Exception {e}!")
        return False
    print("Data read successfully.")
    return True


def lambda_handler(event, context):
    
    print('Reading DynamoDb')
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table("autoscheduler-table")
        stoppedtb=table.scan()
    except Exception as e:
        print(f"DynamoDb Exception {e}!")
        return False
    print("Data read successfully.")
    print(stoppedtb.get('Items', [])[0]['MinSize'])
    for asg in stoppedtb.get('Items', []):
        response = client.update_auto_scaling_group(
            AutoScalingGroupName=asg['ASG_name'],
            MinSize=int(asg['MinSize']),
            MaxSize=int(asg['MaxSize']),
            DesiredCapacity=int(asg['DesiredCapacity']),
        )
    print("ASGs started")
