import os
import glob
import yaml
from distutils.dir_util import copy_tree
import shutil
import argparse
import boto3
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_argparser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--lambda-path',
                        required=True,
                        help='path of src folder of lambda to build '
                             'e.g. src/hello_world',
                        )

    parser.add_argument('--s3-upload',
                        default=False,
                        help='upload lambda to s3 based on config'
                        )

    return parser


def build_zip_with_libs(*, lambda_src):
    config_path = os.path.join(lambda_src, 'config.yml')
    print(config_path)
    with open(config_path, 'r') as stream:
        lambda_cfg = yaml.load(stream)

    conda_env_path = os.path.join(os.environ['HOME'], 'miniconda3')
    site_packages = os.path.join(conda_env_path, 'lib', lambda_cfg['runtime'], 'site-packages')

    # create a tmp path for the lambda function
    tmp_dir = os.path.join('tmp', lambda_src.replace('src/', ''))
    os.makedirs(tmp_dir)

    # copy lambda function content to tmp dir
    r = copy_tree(lambda_src, tmp_dir)

    libs_paths = []
    for l in lambda_cfg['libs']:
        libs_paths.extend(glob.glob(os.path.join(site_packages, l)))

    # copy all libs to
    for p in libs_paths:
        t = copy_tree(p, os.path.join(tmp_dir, p.split('/')[-1]))

    zip_file_dst = os.path.join('dist', lambda_src.split('/')[-1])
    shutil.make_archive(zip_file_dst, 'zip', tmp_dir)

    shutil.rmtree(tmp_dir+'/')
    zip_file = zip_file_dst + '.zip'
    bucket = lambda_cfg['s3_bucket']
    key = lambda_cfg['s3_key']
    return zip_file, bucket, key


def upload_to_s3(*, lambda_zip, bucket, key):
    session = boto3.Session(profile_name='nicor88-aws-dev')
    s3 = session.client('s3')
    res = s3.upload_file(lambda_zip, bucket, key)
    return res

if __name__ == "__main__":
    args = create_argparser().parse_args()
    lambda_path = vars(args).get('lambda_path')
    s3_upload = vars(args).get('s3_upload')
    zip_file, bucket, key = build_zip_with_libs(lambda_src=lambda_path)
    if s3_upload:
        logger.info('Uploading to {}/{} ....'.format(bucket, key))
        res = upload_to_s3(lambda_zip=zip_file, bucket=bucket, key=key)
        logger.info(res)