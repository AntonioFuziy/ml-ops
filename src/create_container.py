import boto3
import os
from dotenv import load_dotenv

load_dotenv()

repository_name = "mlops-project-antoniovf-andretv1"

ecr_client = boto3.client(
  "ecr",
  aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
  region_name=os.getenv("AWS_REGION"),
)

response = ecr_client.create_repository(
  repositoryName=repository_name,
  imageScanningConfiguration={"scanOnPush": True},
  imageTagMutability="MUTABLE",
)

print(response)

print(f"\nrepositoryArn: {response['repository']['repositoryArn']}")
print(f"repositoryUri: {response['repository']['repositoryUri']}")

#repositoryArn: arn:aws:ecr:us-east-2:820926566402:repository/mlops-project-antoniovf-andretv1
#repositoryUri: 820926566402.dkr.ecr.us-east-2.amazonaws.com/mlops-project-antoniovf-andretv1