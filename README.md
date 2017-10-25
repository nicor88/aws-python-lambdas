[![Build Status](https://travis-ci.org/nicor88/aws-python-lambdas.svg?branch=master)](https://travis-ci.org/nicor88/aws-python-lambdas)

# aws-python-lambdas
Collection of python lambda function

## Setup Conda Env
<pre># create env
conda create --name aws-python-lambdas python=3.6.2
# activate env
source activate aws-python-lambdas
pip install boto3
pip install pytest
# install libs from the requirements of each single lambda
for i in src/*/; do pip install -r $i"requirements.txt"; done
</pre>

# Structure

<pre>
└── src/
    ├── hello_world_lambda
    │    ├── __init__.py
    │    ├── requirements.txt
    │    └── lambda_function.py
    └── lambda_function_test_
         ├── __init__.py
         ├── requirements.txt
         └── lambda_function.py            
</pre>

Where:
*  requirements.txt: contains the libs needed by the lambda
*  lambda_function.py contains the lambda handler
<pre>def lambda_handler(event, context):
    something = 'hello_world'
    return something
</pre>
