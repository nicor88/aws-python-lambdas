import boto3

print('Loading function')

def lambda_handler(event, context):
    print(event)
    payLoad = {}

    payLoad['Purpose'] = '{} '.format(event['RequestType'])

    # example failing status
    # cfnresponse.send(event, context, cfnresponse.FAILED, payLoad)

    cfnresponse.send(event, context, cfnresponse.SUCCESS, payLoad)
    return payLoad
