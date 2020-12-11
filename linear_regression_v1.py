import numpy as np
import pandas as pd

from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_absolute_error

data_raw = pd.read_csv('books.csv', error_bad_lines=False)

x = data_raw[['num_pages','ratings_count','text_reviews_count']]
y = data_raw.average_rating
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=42)

trainer = xgb.XGBRegressor()
trainer.fit(x_train, y_train)

prediction_train = trainer.predict(x_train)
prediction_test = trainer.predict(x_test)
print(y_test)
print(prediction_test)

print("MAE:", mean_absolute_error(y_test, prediction_test))