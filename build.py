import boto3
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

    parser.add_argument('--s3-upload',
                        default=False,
                        help='upload lambda to s3 based on config'
                        )


    return parser


def create_zip(*, src, dst):
    # get lambda config
    lambda_cfg = yaml.load(resource_string(src.replace('/', '.'), 'config.yml'))
    lambda_name_zip = '{}.zip'.format(src.split('/')[1])
    logger.info('Building lambda {}'.format(src.split('/')[1]))
    logger.debug(lambda_cfg)
    logger.info('Source folder {}'.format(src_path))
    logger.info('Destination folder {}'.format(dist_path))
    final_destination = '{}/{}'.format(dst, lambda_name_zip)
    subprocess.call(['zip', '-j', '-r', final_destination, src, ])
    return lambda_cfg, final_destination


def upload_to_s3(*, lambda_zip, bucket, key):
    session = boto3.Session(profile_name='nicor88-aws-dev')
    s3 = session.client('s3')
    s3.upload_file(lambda_zip, bucket, key)

if __name__ == "__main__":
    args = create_argparser().parse_args()
    src_path = vars(args).get('src_path')
    dist_path = vars(args).get('dist_path')
    s3_upload = vars(args).get('s3_upload')
    cfg, final_dst = create_zip(src=src_path, dst=dist_path)
    logger.debug(final_dst)
    if s3_upload:
        logger.info('Uploading to {}/{} ....'.format(cfg['s3_bucket'], cfg['s3_key']))
        upload_to_s3(lambda_zip=final_dst, bucket=cfg['s3_bucket'], key=cfg['s3_key'])

