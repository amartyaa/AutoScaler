import os
import boto3
from datetime import datetime

print("Lambda_trigerred at ", datetime.now())





dynamodb = boto3.resource('dynamodb')

def Read_data_in_database():
    print('Reading DynamoDb')
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ["TABLE_NAME"])
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
        table = dynamodb.Table(os.environ["TABLE_NAME"])
        stoppedtb=table.scan()
    except Exception as e:
        print(f"DynamoDb Exception {e}!")
        return False
    print("Data read successfully.")
    
    for asg in stoppedtb.get('Items', []):
        client = boto3.client('autoscaling',region_name = asg['Region'])
        check = client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                asg['Name']
            ],
            )
        if(check['AutoScalingGroups'] !=[] ):
            response = client.update_auto_scaling_group(
            AutoScalingGroupName=asg['Name'],
            MinSize=int(asg['MinSize']),
            MaxSize=int(asg['MaxSize']),
            DesiredCapacity=int(asg['DesiredCapacity']),
        )
        else:
            print(asg['Name'],'not found in AutoScaling Groups')
    print("All ASGs scaled up")
    
    for region in os.environ["REGIONS"].split(","):
        ec2 = boto3.resource('ec2',region_name=region)
        Ec2ScaleUp(ec2,region)
    
def Ec2ScaleUp(ec2,region):
    label = str(os.environ['EC2_LABEL']).split(":")
    if label!="all":
        key = "tag:"+label[0]
        value = []
        value.append(label[1])
        filters=[
                {'Name': 'instance-state-name', 'Values': ['stopped']},
                {'Name': key,            'Values': value}
            ]
    else:
        filters=[
                {'Name': 'instance-state-name', 'Values': ['stopped']},
            ]
    # print(type(filters))
    instances = ec2.instances.filter(Filters=filters)
    instances.start()