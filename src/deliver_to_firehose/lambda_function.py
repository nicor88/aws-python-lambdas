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
    delivery_stream = os.environ['DELIVERY_STREAM']

    firehose = boto3.client('firehose')

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
