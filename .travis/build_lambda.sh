LAMBDA_PATH=$1
SRC=src/
LAMBDA_NAME=${LAMBDA_PATH#${SRC}}
LAMBDA_NAME=${LAMBDA_NAME%/}

echo Building $LAMBDA_NAME inside $LAMBDA_PATH


pip install -r $LAMBDA_PATH"requirements.txt" -t $LAMBDA_PATH --upgrade

cd $LAMBDA_PATH
zip -r $LAMBDA_NAME.zip .
mv $LAMBDA_NAME.zip ..

# for i in src/*/; do .travis/build.sh "$i"; done
