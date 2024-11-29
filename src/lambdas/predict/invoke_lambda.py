import boto3
import os
import botocore

cfg = botocore.config.Config(
  retries={ 'max_attempts': 0 }, 
  read_timeout=840,
  connect_timeout=600,
  region_name=os.getenv("AWS_REGION") 
)

lambda_client = boto3.client(
  "lambda",
  config=cfg,
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
  region_name=os.getenv("AWS_REGION"),
)

response = lambda_client.invoke(
  FunctionName='predict_antoniovf_andretv1_project',
  Payload='{}',
)

print(response["Payload"].read().decode("utf-8"))
