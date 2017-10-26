import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def lambda_handler(event, context):
    if 'stack_name' in event.keys():
        stack_name = event['stack_name']
    else:
        raise KeyError('no stack_name provided')

    cfn = boto3.client('cloudformation')
    cfn.delete_stack(StackName=stack_name)
    msg = 'Delete request for {} Cloudformation sent'.format(stack_name)
    logger.info(msg)
    return msg
