from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
from datetime import datetime
import boto3
import logging

today = datetime.now().date()

s3_client = boto3.client("s3")

bucket_name = "mlops-project-antoniovf-andretv1"

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

def train():
  s3_data = s3_client.get_object(Bucket=bucket_name, Key=f"data/process/train-housing-{today}.csv")
  df = pd.read_csv(s3_data["Body"])
  
  try:
    write_log("info", f"Dropping target column...")
    X = df.drop(columns=['median_house_value'], axis=1)
    Y = df['median_house_value']

    write_log("info", f"Splitting data...")
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=100)
    mms = MinMaxScaler(feature_range=(0, 1))
    x_train = mms.fit_transform(x_train)
    x_test = mms.transform(x_test)

    kernels = [
      ('linear', 'auto', 3, 1),
      ('rbf', 6, 3, 5),
      ('poly', 'scale', 2, 1)
    ]

    for kernel_type, gamma_value, degree_value, c_value in kernels:
      write_log("info", f"Training model with {kernel_type} kernel...")
      svr = SVR(
        kernel=kernel_type, 
        gamma=gamma_value, 
        degree=degree_value,
        C=c_value
      )
      svr.fit(x_train, y_train)
      write_log("info", f"model {kernel_type} kernel got {svr.score(x_test, y_test)}")

      model_file_path = f"models/{kernel_type}-{today}.pkl"
      tmp_model_file_path = f"/tmp/{kernel_type}.pkl"
      write_log("info", f"Saving model to {model_file_path}...")
      with open(tmp_model_file_path, "wb") as f:
        pickle.dump(svr, f)
        
      s3_client.upload_file(tmp_model_file_path, bucket_name, model_file_path)

  except Exception as e:
    write_log("error", e)
    write_log("error", "Training Failed!")
  
def handler(event, context):
  write_log("info", "Starting Training...")
  train()
  write_log("info", "Training Done!")

  return {
    "statusCode": 200,
    "body": "All Training done!"
  }