import pytest
import boto3


def test_emr_describe_cluster():
    cfn = boto3.client('emr')
    assert hasattr(cfn, 'describe_cluster')

