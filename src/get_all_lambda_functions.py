import boto3
import os
from dotenv import load_dotenv

load_dotenv()

lambda_client = boto3.client(
  "lambda",
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
  region_name=os.getenv("AWS_REGION"),
)

response = lambda_client.list_functions(MaxItems=1000)

functions = response["Functions"]

print(f"You have {len(functions)} Lambda functions")

if len(functions) > 0:
  print("Here are their names:")

print(len(functions))

for function in functions:
  function_name = function["FunctionName"]
  print(function_name)