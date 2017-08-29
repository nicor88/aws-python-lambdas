import base64
import botocore.exceptions
import os
import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # config lambda variables
    logger.info(event)
    add_newline = os.environ['ADD_NEWLINE']
    cross_account_role_arn = os.environ['CROSS_ACCOUNT_ROLE_ARN']
    delivery_stream = os.environ['DELIVERY_STREAM']

    # assume cross-account role
    client = boto3.client('sts')

    # TODO dont know if is needed
    sts_response = client.assume_role(
        RoleArn=cross_account_role_arn,
        RoleSessionName='AssumeRoleSession', DurationSeconds=900)

    firehose = boto3.client('firehose',
                            aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                            aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                            aws_session_token=sts_response['Credentials']['SessionToken'])

    records = event['Records']

    res = None
    if add_newline == 'True':
        records_acc = []
        for r in records:
            record = json.loads(base64.b64decode(r['kinesis']['data']).decode())
            record['sequenceNumber'] = r['kinesis']['sequenceNumber']
            data_with_separator = str(record) + '\n'
            logger.info(data_with_separator.encode())
            record_for_firehose = {'Data': data_with_separator.encode()}
            try:
                res = firehose.put_record(DeliveryStreamName=delivery_stream,
                                          Record=record_for_firehose)
                records_acc.append(record_for_firehose)
            except botocore.exceptions.ClientError as err:
                message = err.response['Error']['Message']
                res = message
                logger.error(res)

        logger.info('{} Records were put to {}'.format(len(records_acc),
                                                            delivery_stream))
    else:
        records_for_firehose = [{'Data': base64.b64decode(r['kinesis']['data'])} for r in
                                records]
        logger.debug('Putting {} records to {}'.format(len(records_for_firehose), delivery_stream))
        try:
            res = firehose.put_record_batch(DeliveryStreamName=delivery_stream,
                                        Records=records_for_firehose)
        except botocore.exceptions.ClientError as err:
            message = err.response['Error']['Message']
            res = message
            logger.error(res)
    return res
