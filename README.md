# aws-python-lambdas
Collection of python lambda function

## Setup Conda Env
<pre># create env
conda env create -n aws-python-lambdas -f conda-dev-env.yml
# activate env
source activate aws-python-lambdas
# after installing new libs update conda-dev-env.yml
conda env export --file conda-dev-env.yml 
</pre>

## Building

<pre># build lambda function contained inside src/hello_world
python build.py --src-path src/hello_world --dist-path dist
</pre>

By default the upload to S3 is disabled, but it's possible to 
upload the lambda to S3 based on the config specified for each lambdas
running the following command:
<pre># upload to s3
python build.py --src-path src/hello_world --dist-path dist --s3-upload True
</pre>


# Structure

<pre>
└── src/
    ├── hello_world_lambda
    │    ├── __init__.py      
    │    ├── config.yml
    │    └── lambda_function.py
    └── lambda_function_test_
         ├── __init__.py      
         ├── config.yml
         └── lambda_function.py            
</pre>

Where:
*  init.py is an empty file used during the building to retrieve th yml
*  config.yml contain the config of the lambda (e.g. s3_bucket, s3_key, libs needed for the lambda)
*  lambda_function.py contains the real lambda with this structure
<pre>def lambda_handler(event, context):
    something = 'hello_world'
    return something
</pre>
