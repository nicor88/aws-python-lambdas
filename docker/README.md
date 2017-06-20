## Amazon Linux Container

## Build Docker Image
<pre>
docker build --rm=True --tag "nicor88/aws-linux-lambda" .
</pre>

## Run
<pre># python version
docker run --rm nicor88/aws-linux-lambda:latest python --version

# bin bash
docker run -i -t nicor88/aws-linux-lambda:latest /bin/bash

# copy libs
docker run -v $(pwd):/outputs -it nicor88/aws-linux-lambda:latest /bin/bash /outputs/copy_libs.sh
</pre>
