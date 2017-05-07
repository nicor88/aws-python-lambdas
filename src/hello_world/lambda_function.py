import boto3

print('Loading function')


def lambda_handler(event, context):
    print(event)
    return event
