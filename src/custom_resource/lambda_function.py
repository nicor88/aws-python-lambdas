import boto3
import cfnresponce

print('Loading function')

def lambda_handler(event, context):
    print(event)
    payLoad = {}

    payLoad['Purpose'] = '{} a custom resource'.format(event['RequestType'])

    cfnresponse.send(event, context, cfnresponse.SUCCESS, payLoad)
    return payLoad
