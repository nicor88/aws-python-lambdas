import yaml
import numpy as np
# import pandas as pd

print('Loading function')


def lambda_handler(event, context):
    # print(pd.__version__)
    print(np.__version__)
    with open('config.yml', 'r') as stream:
        data_loaded = yaml.load(stream)
    print(data_loaded)
    return data_loaded
