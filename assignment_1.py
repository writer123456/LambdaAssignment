import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Find all instances with the Auto-Stop tag
    stop_instances = find_instances_by_tag(ec2, 'Auto-Stop')
    if stop_instances:
        print(f'Stopping instances: {stop_instances}')
        ec2.stop_instances(InstanceIds=stop_instances)

    # Find all instances with the Auto-Start tag
    start_instances = find_instances_by_tag(ec2, 'Auto-Start')
    if start_instances:
        print(f'Starting instances: {start_instances}')
        ec2.start_instances(InstanceIds=start_instances)
    
    return {
        'statusCode': 200,
        'body': 'Auto-Start and Auto-Stop actions executed successfully.'
    }

def find_instances_by_tag(ec2, tag):
    # Describe instances with the specified tag
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': f'tag:{tag}',
                'Values': ['true']
            }
        ]
    )

    # Collect all instance IDs
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])

    return instances
