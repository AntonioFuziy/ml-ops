import boto3
import os
from dotenv import load_dotenv

load_dotenv()

function_name = "${LAMBDA_NAME}_antoniovf_andretv1_v3"

image_uri = "${ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/mlops-project-antoniovf-andretv1:${LAMBDA_NAME}"

lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN_PROJECT")

lambda_client = boto3.client(
  "lambda",
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
  region_name=os.getenv("AWS_REGION"),
)

response = lambda_client.create_function(
  FunctionName=function_name,
  PackageType="Image",
  Code={"ImageUri": image_uri},
  Role=lambda_role_arn,
  Timeout=200,
  MemorySize=128,
)

print("Lambda function created successfully:")
print(f"Function Name: {response['FunctionName']}")
print(f"Function ARN: {response['FunctionArn']}")