import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

test_event = {
  "Records": [
    {
      "eventVersion": "2.0",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "s3": {
        "configurationId": "testConfigRule",
        "object": {
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901",
          "key": "csv/SampleCSVFile_2kb.csv",
          "size": 1024
        },
        "bucket": {
          "arn": "arn:aws:s3:::nicor-data",
          "name": "nicor-data",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          }
        },
        "s3SchemaVersion": "1.0"
      },
      "responseElements": {
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
        "x-amz-request-id": "EXAMPLE123456789"
      },
      "awsRegion": "us-east-1",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "eventSource": "aws:s3"
    }
  ]
}


def lambda_handler(event, context):
    email_content = ''
    s3 = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info('Reading {} from {}'.format(file_key, bucket_name))
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    lines = obj['Body'].read().split(b'\n')
    for r in lines:
        logger.info(r.decode())
        email_content = email_content + '\n' + r.decode()
    logger.info(email_content)

# lambda_handler(test_event, '')
