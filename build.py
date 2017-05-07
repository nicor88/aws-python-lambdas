import argparse
import ruamel_yaml as yaml
import subprocess
import logging
from pkg_resources import resource_string
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def create_argparser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--src-path',
                        required=True,
                        help='path of src folder of lambda to build '
                             'e.g. src/hello_world',
                        )

    parser.add_argument('--dist-path',
                        required=True,
                        help='destination path of the build lambda '
                             'e.g. dist',
                        )

    return parser


def create_zip(*, src, dst):
    # get lambda config
    cfg = yaml.load(resource_string(src.replace('/', '.'), 'config.yml'))
    lambda_name_zip = '{}.zip'.format(src.split('/')[1])
    logger.info('Building lambda {}'.format(src.split('/')[1]))
    logger.debug(cfg)
    logger.info('Source folder {}'.format(src_path))
    logger.info('Destination folder {}'.format(dist_path))
    final_destination = '{}/{}'.format(dst, lambda_name_zip)
    subprocess.call(['zip', '-j', '-r', final_destination, src])


if __name__ == "__main__":
    args = create_argparser().parse_args()
    src_path = vars(args).get('src_path')
    dist_path = vars(args).get('dist_path')
    create_zip(src=src_path, dst=dist_path)
