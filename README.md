# AutoScaler
> Main goal while creating this is to **cut the cost of running instances** in dev environment during off period *{ Night or Weekend or Vacations}*

>Works only in a particular region where you implement it

### CloudFormation Template: 

Create stack using this template to scale-down all autoscaling groups to 0,0,0 after given time and then scale back them up to retained configurations. Creates two lambda functions which handle all the steps.

### Lambdas:
> Support Lambdas for the CFN template

#### stopASG_lambda.py
>> Stores the meta data of ASGs into DynamoDB and then scales them down to {0,0,0}.

DynamoDB Config

|ASG_name | LastShutDownAt | DesiredCapacity | MaxSize | MinSize|
| --- | :---: | :---: | :---: | :---: |
|"name of ASG" | time | 4 | 6 | 2|

#### startASG_lambda.py 
>> scales up to all the ASG to configuration in accordance to database


### Terraform File (*main.tf*)
>> Designs two resources of *aws_autoscaling_schedule* which attach to all the ASGs in region and scaled them back to 2,4,2.