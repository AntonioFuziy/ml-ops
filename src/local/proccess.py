import pandas as pd
from sklearn.preprocessing import PowerTransformer
from datetime import datetime
from log import write_log
from impute_knn import impute_knn

today = datetime.now().date()

df_raw = pd.read_csv("../../data/housing.csv")

try: 
  df = impute_knn(df_raw)

  df['mean_num_family'] = df['population'] / df['households']
  df = df.drop(columns=['mean_num_family','ocean_proximity','households','total_bedrooms','population','longitude','latitude'], axis=1)

  df = pd.DataFrame(PowerTransformer().fit_transform(df), columns=df.columns)

  df.to_parquet(f"../../data/train-housing-{today}.parquet")

  write_log("info", f"Saved to ../../data/train-housing-{today}.parquet")
  write_log("info", "Pre-Processing Done!")
except Exception as e:
  write_log("error", e)
  write_log("error", "Pre-Processing Failed!")