import logging
import yaml

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def lambda_handler(event, context):
    # loading yaml
    with open('config.yml', 'r') as stream:
        data_loaded = yaml.load(stream)
    logger.info(data_loaded)
    return data_loaded
