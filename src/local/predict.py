import pandas as pd
import sys
import pickle
import os
from log import write_log
import warnings

warnings.filterwarnings("ignore")

df_path = sys.argv[1]
df = pd.read_parquet(df_path)

try:
  df = df.drop("median_house_value", axis=1)
  write_log("info", "Dropped target column")
  
  df_predict = df.copy()

  folder_path = '../../models'

  for filename in os.listdir(folder_path):
    if filename.endswith('.pkl'):
      file_path = os.path.join(folder_path, filename)

      with open(file_path, 'rb') as file:
        model = pickle.load(file)
        write_log("info", f"Loading model file {file_path}...")

        y_pred = model.predict(df)
        write_log("info", f"Predicting with {file_path}...")

        write_log("info", f"{file_path} prediction result: {y_pred}")
        df_predict[f"median_house_value_{filename}"] = y_pred

except Exception as e:
  write_log("error", e)
  write_log("error", "Prediction Failed!")