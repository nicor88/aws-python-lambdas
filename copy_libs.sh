#!/bin/bash
set -ex

conda install -y numpy

echo $CONDA_DIR

SITE_PACKAGES="$CONDA_DIR/lib/python3.6/site-packages"

cp -R $SITE_PACKAGES/numpy /outputs/libs_amazon_linux

cp $CONDA_DIR/lib/*.so /outputs/libs_amazon_linux
