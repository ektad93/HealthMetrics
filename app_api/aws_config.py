import boto3

AWS_ACCESS_KEY = 'AWS ACCESS KEY'
AWS_SECRET_KEY = 'AWS SECRET KEY'
S3_BUCKET = 'your s3 default bucket'
DEAFULT_REGION = 'us-east-2'


session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=DEAFULT_REGION
)
