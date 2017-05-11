import base64
import boto3
import os

print('Loading function')


def lambda_handler(event, context):
    firehose = boto3.client('firehose')
    records = event['Records']
    records_for_firehose = [{'Data': base64.b64decode(r['kinesis']['data'])} for r in records]
    delivery_stream = os.environ['DELIVERY_STREAM']
    res_firehose = firehose.put_record_batch(DeliveryStreamName=delivery_stream,
                                             Records=records_for_firehose)

    return res_firehose
