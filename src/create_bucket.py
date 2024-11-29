import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
  "s3",
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

s3.create_bucket(Bucket='mlops-project-antoniovf-andretv1', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})