import boto3
from cfnresponce import send, SUCCESS

print('Loading function')

def lambda_handler(event, context):
    print(event)
    payLoad = {}

    payLoad['Purpose'] = '{} '.format(event['RequestType'])

    # example failing status
    # cfnresponse.send(event, context, cfnresponse.FAILED, payLoad)

    send(event, context, SUCCESS, payLoad)
    return payLoad
