import boto3
from cfnresponce import send, SUCCESS, FAILED

print('Loading function')

def lambda_handler(event, context):
    print(event)
    payLoad = {}

    payLoad['Purpose'] = '{} a custom resource'.format(event['RequestType'])

    # example failing status
    # send(event, context, FAILED, payLoad)

    send(event, context, SUCCESS, payLoad)
    return payLoad
