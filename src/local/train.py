from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import sys
from datetime import datetime
from log import write_log

today = datetime.now().date()

df_path = sys.argv[-1]

df = pd.read_parquet(df_path)

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

    file_path = f"../../models/{kernel_type}-{today}.pkl"
    write_log("info", f"Saving model to {file_path}...")
    with open(file_path, "wb") as f:
      pickle.dump(svr, f)
except Exception as e:
  write_log("error", e)
  write_log("error", "Training Failed!")