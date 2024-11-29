import boto3
import os
from dotenv import load_dotenv
from datetime import datetime

today = datetime.now().date()

load_dotenv()

s3 = boto3.client(
  "s3",
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

s3.upload_file("../data/housing.csv", "mlops-project-antoniovf-andretv1", f"data/raw/housing-{today}.csv")