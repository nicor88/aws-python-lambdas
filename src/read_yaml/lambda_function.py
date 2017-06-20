import yaml

print('Loading function')


def lambda_handler(event, context):
    # loading yaml
    with open('config.yml', 'r') as stream:
        data_loaded = yaml.load(stream)
    print(data_loaded)
    return data_loaded
