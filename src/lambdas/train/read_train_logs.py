import os
import boto3
from dotenv import load_dotenv

load_dotenv()

function_name = "train_antoniovf_andretv1_project"
lambda_group_name = f"/aws/lambda/{function_name}"

session = boto3.Session(
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
  region_name=os.getenv("AWS_REGION"),
)

logs_client = session.client("logs")

response = logs_client.describe_log_streams(
  logGroupName=lambda_group_name
)

log_stream_name = response["logStreams"][0]["logStreamName"]

log_events = logs_client.get_log_events(
  logGroupName=lambda_group_name,
  logStreamName=log_stream_name,
)

for i, event in enumerate(log_events["events"]):
  print(event["message"])

  if event != len(log_events["events"]) - 1:
    print("-" * 60)
    print(f"LOG {i+1}:")
  print(event["message"])