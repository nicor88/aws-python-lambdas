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
pip install -r requirements.txt
</pre>

# Structure

<pre>
└── src/
    ├── hello_world_lambda
    │    ├── __init__.py
    │    └── lambda_function.py
    └── lambda_function_test_
         ├── __init__.py
         └── lambda_function.py            
</pre>

Where:
*  init.py is an empty file used during the building to retrieve th yml
*  lambda_function.py contains the lambda handler
<pre>def lambda_handler(event, context):
    something = 'hello_world'
    return something
</pre>
