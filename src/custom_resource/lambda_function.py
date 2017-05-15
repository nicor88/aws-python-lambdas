import boto3
import cfnresponse

print('Loading function')

def lambda_handler(event, context):
    print(event)
    payLoad = {}

    payLoad['Purpose'] = '{} a custom resource'.format(event['RequestType'])

    # example failing status
    # cfnresponse.send(event, context, cfnresponse.FAILED, payLoad)

    cfnresponse.send(event, context, cfnresponse.SUCCESS, payLoad)
    return payLoad
