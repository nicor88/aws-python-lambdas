import boto3
import cfnresponce

print('Loading function')

def lambda_handler(event, context):
    print(event)
    payLoad = {}

    payLoad['Purpose'] = '{} a custom resource'.format(event['RequestType'])

    # example failing status
    # cfnresponce.send(event, context, cfnresponce.FAILED, payLoad)

    cfnresponce.send(event, context, cfnresponce.SUCCESS, payLoad)
    return payLoad
