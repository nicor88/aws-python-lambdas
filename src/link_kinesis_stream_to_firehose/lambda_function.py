import base64
import boto3
import botocore.exceptions
import os

print('Loading function')


def lambda_handler(event, context):
    firehose = boto3.client('firehose')
    records = event['Records']
    records_for_firehose = [{'Data': base64.b64decode(r['kinesis']['data'])} for r in records]
    delivery_stream = os.environ['DELIVERY_STREAM']
    print('Putting {} records to {}'.format(len(records_for_firehose), delivery_stream))

    res = None
    try:
        res = firehose.put_record_batch(DeliveryStreamName=delivery_stream,
                                        Records=records_for_firehose)
    except botocore.exceptions.ClientError as err:
        message = err.response['Error']['Message']
        res = message
    return res
