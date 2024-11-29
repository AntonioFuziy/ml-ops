import pandas as pd
import pickle
import boto3
from datetime import datetime 
import logging
from io import StringIO

today = datetime.now().date()
bucket_name = "mlops-project-antoniovf-andretv1"

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")

def write_log(_type, message):
  logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
  )
  if _type == "info":
    logging.info(message)
    print(f"{_type}: {message}")
  elif _type == "warning":
    logging.warning(message)
    print(f"{_type}: {message}")
  elif _type == "error":
    logging.error(message)
    print(f"{_type}: {message}")
  elif _type == "critical":
    logging.critical(message)
    print(f"{_type}: {message}")
  else:
    logging.debug(message)
    print(f"{_type}: {message}")

def predict():
  s3_data = s3_client.get_object(Bucket=bucket_name, Key=f"data/process/train-housing-{today}.csv")
  df = pd.read_csv(s3_data["Body"])

  try:
    df = df.drop("median_house_value", axis=1)
    write_log("info", "Dropped target column")
    
    df_predict = df.copy()

    folder_path = 'models'
    objects = s3_client.list_objects(Bucket=bucket_name, Prefix=folder_path)
    filtered_paths = [path['Key'] for path in objects.get('Contents', []) if f'{today}' in path['Key']]

    for filename in filtered_paths:
      if 'rbf' in filename:
        response = s3_client.get_object(Bucket=bucket_name, Key=filename)
        model = pickle.loads(response['Body'].read())

        write_log("info", f"Loading model file {filename}...")

        y_pred = model.predict(df)
        write_log("info", f"Predicting with {filename}...")

        write_log("info", f"{filename} prediction result: {y_pred}")
        df_predict[f"median_house_value_{filename}"] = y_pred

        write_log("info", f"Saving prediction file {filename}...")
        csv_buffer = StringIO()
        df_predict.to_csv(csv_buffer)
        s3_resource.Object(bucket_name, f"data/predict/predict-housing-{today}.csv").put(Body=csv_buffer.getvalue())

  except Exception as e:
    write_log("error", e)
    write_log("error", "Prediction Failed!")

def handler(event, context):
  write_log("info", "Starting Prediction...")
  predict()
  write_log("info", "Prediction Done!")

  return {
    "statusCode": 200,
    "body": "Prediction Done!"
  }