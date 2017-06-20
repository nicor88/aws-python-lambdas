import logging
import numpy as np
# import pandas as pd


logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')


def lambda_handler(event, context):
    logger.info('numpy version is {}'.format(np.__version__))
    # lib_version = {'numpy': np.__version__, 'pandas': pd.__version__}
    lib_version = {'numpy': np.__version__}
    return lib_version
