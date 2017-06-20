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
    libs_to_exclude = ['boto3', 'botocore', 'numpy']
    config_path = os.path.join(lambda_src, 'config.yml')
    print(config_path)
    with open(config_path, 'r') as stream:
        lambda_cfg = yaml.load(stream)
    conda_env_name = 'aws-python-lambdas'
    conda_path = os.path.join(os.environ['HOME'], 'miniconda3')
    conda_pkgs_path = os.path.join(os.environ['HOME'], 'miniconda3', 'pkgs')
    conda_env_path = os.path.join(conda_path, 'envs', conda_env_name)
    site_packages = os.path.join(conda_env_path, 'lib', lambda_cfg['runtime'], 'site-packages')

    # create a tmp path for the lambda function
    tmp_dir = os.path.join('tmp', lambda_src.replace('src/', ''))
    os.makedirs(tmp_dir)

    # copy lambda function content to tmp dir
    r = copy_tree(lambda_src, tmp_dir)

    libs_paths = []
    libs = [l for l in lambda_cfg['libs'] if not l in libs_to_exclude]
    for l in libs:
        lib_path = os.path.join(site_packages, l)
        logger.info(glob.glob(lib_path))
        lib_files = glob.glob(os.path.join(site_packages, l))
        if len(lib_files) == 0:
            logger.debug('trying to add single file')
            lib_path = os.path.join(site_packages, l) + '.py'
            lib_files = glob.glob(lib_path)
            logger.info('Found {}'.format(lib_files))
        libs_paths.extend(lib_files)

    # copy all libs to
    for p in libs_paths:
        if '.py' in p:
            logger.info('Copying file {} to {}'.format(p, tmp_dir))
            shutil.copy2(p, tmp_dir)
        else:
            dst = os.path.join(tmp_dir, p.split('/')[-1])
            logger.info('Copying tree path {} to {}'.format(p, dst))
            t = copy_tree(p, dst)

    if 'numpy' in lambda_cfg['libs']:
        logger.info('Use already builded version of numpy')
        t = copy_tree('libs_amazon_linux/numpy', os.path.join(tmp_dir, 'numpy'))
        #so_libs = glob.glob('libs_amazon_linux/libmkl_*.so')
        #logger.info(so_libs)
        #for so_p in so_libs:
        #   shutil.copy2(so_p, tmp_dir)
        shutil.copy2('libs_amazon_linux/libmkl_intel_lp64.so', tmp_dir)
        shutil.copy2('libs_amazon_linux/libmkl_intel_thread.so', tmp_dir)
        shutil.copy2('libs_amazon_linux/libmkl_core.so', tmp_dir)
        shutil.copy2('libs_amazon_linux/libiomp5.so', tmp_dir)

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
