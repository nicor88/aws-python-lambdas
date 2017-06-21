import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def lambda_handler(event, context):
    logger.info(event)
    output = {'purpose': 'Hello World'}
    return output
