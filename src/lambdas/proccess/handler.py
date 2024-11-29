import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import PowerTransformer
from datetime import datetime
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsRegressor
import boto3
from io import StringIO

today = datetime.now().date()

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")

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

def impute_knn(df):
  ldf = df.select_dtypes(include=[np.number])
  ldf_putaside = df.select_dtypes(exclude=[np.number])
  cols_nan = ldf.columns[ldf.isna().any()].tolist()
  cols_no_nan = ldf.columns.difference(cols_nan).values
  
  write_log("info", f"Imputing {cols_nan} with KNN...")

  for col in cols_nan:
    imp_test = ldf[ldf[col].isna()]
    imp_train = ldf.dropna()
    model = KNeighborsRegressor(n_neighbors=5)
    knr = model.fit(imp_train[cols_no_nan], imp_train[col])
    ldf.loc[df[col].isna(), col] = knr.predict(imp_test[cols_no_nan])
    
  return pd.concat([ldf, ldf_putaside], axis=1)

def proccess():
  s3_data = s3_client.get_object(Bucket=bucket_name, Key=f"data/raw/housing-{today}.csv")
  df_raw = pd.read_csv(s3_data["Body"])

  try: 
    df = impute_knn(df_raw)

    df['mean_num_family'] = df['population'] / df['households']
    df = df.drop(columns=['mean_num_family', 'ocean_proximity', 'households', 'total_bedrooms', 'population', 'longitude', 'latitude'], axis=1)

    df = pd.DataFrame(PowerTransformer().fit_transform(df), columns=df.columns)

    print(df.head())

    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket_name, f"data/process/train-housing-{today}.csv").put(Body=csv_buffer.getvalue())

    write_log("info", f"Saved to data/proccess/train-housing-{today}.csv")
  
  except Exception as e:
    write_log("error", e)
    write_log("error", "Pre-Processing Failed!")

def handler(event, context):
  write_log("info", "Starting Pre-Processing...")
  proccess()
  write_log("info", "Pre-Processing Done!")

  return {
    "statusCode": 200,
    "body": "All pre-processing done!"
  }