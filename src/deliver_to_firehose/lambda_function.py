import base64
import botocore.exceptions
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    # config lambda variables
    cross_account_role_arn = os.environ['CROSS_ACCOUNT_ROLE_ARN']
    region_name = os.environ['AWS_REGION_NAME']
    delivery_stream = os.environ['DELIVERY_STREAM']

    # assume cross-account role
    client = boto3.client('sts')
    sts_response = client.assume_role(
        RoleArn=cross_account_role_arn,
        RoleSessionName='AssumeDataEngRole', DurationSeconds=900)

    firehose = boto3.resource(service_name='firehose',
                              region_name=region_name,
                              aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                              aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                              aws_session_token=sts_response['Credentials']['SessionToken'])

    records = event['Records']
    records_for_firehose = [{'Data': base64.b64decode(r['kinesis']['data'])} for r in records]

    logger.debug('Putting {} records to {}'.format(len(records_for_firehose), delivery_stream))

    res = None
    try:
        res = firehose.put_record_batch(DeliveryStreamName=delivery_stream,
                                        Records=records_for_firehose)
    except botocore.exceptions.ClientError as err:
        message = err.response['Error']['Message']
        res = message
        logger.debug(res)
    return res
