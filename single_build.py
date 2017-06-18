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

lambda_src = 'src/read_yaml'
config_path = os.path.join(lambda_src, 'config.yml')
print(config_path)
with open(config_path, 'r') as stream:
    lambda_cfg = yaml.load(stream)
conda_env_name = 'aws-python-lambdas'
conda_env_path = os.path.join(os.environ['HOME'], 'miniconda3', 'envs', conda_env_name)
site_packages = os.path.join(conda_env_path, 'lib', lambda_cfg['runtime'], 'site-packages')

# create a tmp path for the lambda function
tmp_dir = os.path.join('tmp', lambda_src.replace('src/', ''))
os.makedirs(tmp_dir)

# copy lambda function content to tmp dir
r = copy_tree(lambda_src, tmp_dir)

libs_paths = []
for l in lambda_cfg['libs']:
    lib_path = os.path.join(site_packages, l)
    lib_files = glob.glob(lib_path)
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
        shutil.copy2(p, tmp_dir )
    else:
        dst = os.path.join(tmp_dir, p.split('/')[-1])
        logger.info('Copying tree path {} to {}'.format(p, dst))
        t = copy_tree(p, dst)
    # logger.info(t)

zip_file_dst = os.path.join('dist', lambda_src.split('/')[-1])
shutil.make_archive(zip_file_dst, 'zip', tmp_dir)

# shutil.rmtree(tmp_dir+'/')
zip_file = zip_file_dst + '.zip'
bucket = lambda_cfg['s3_bucket']
key = lambda_cfg['s3_key']
