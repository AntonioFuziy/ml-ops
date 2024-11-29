from sklearn.neighbors import KNeighborsRegressor
from log import write_log
import pandas as pd
import numpy as np

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