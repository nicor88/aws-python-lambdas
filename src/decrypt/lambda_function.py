from base64 import b64decode
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def lambda_handler(event, context):
    encrypted = os.environ['ENCRYPTED_VALUE']
    decrypted = boto3.client('kms').decrypt(CiphertextBlob=b64decode(encrypted))['Plaintext']
    decrypted = decrypted.decode()
    logger.info(f'encrypted: {encrypted} decrypted: {decrypted}')
