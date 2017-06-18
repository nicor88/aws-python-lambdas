import pytest
import boto3


def test_cfn_create_stack():
    cfn = boto3.client('cloudformation')
    assert hasattr(cfn, 'create_stack')


def test_cfn_delete_stack():
    cfn = boto3.client('cloudformation')
    assert hasattr(cfn, 'delete_stack')
