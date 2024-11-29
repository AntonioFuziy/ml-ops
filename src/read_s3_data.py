import boto3
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

today = datetime.now().date()

s3 = boto3.client(
  "s3",
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

bucket_name = "mlops-project-antoniovf-andretv1"

objects = s3.list_objects(Bucket=bucket_name, Prefix="")
# filtered_paths = [path['Key'] for path in objects.get('Contents', []) if f'2023-11-08' in path['Key']]
# print(filtered_paths)
for obj in objects.get('Contents', []):
  print('File:', obj['Key'])