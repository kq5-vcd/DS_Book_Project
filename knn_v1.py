import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv('goodreads/actual_data.csv')

conditions = [
    (data['Rate'] < 3),
    (data['Rate'] >= 3) & (data['Rate'] < 3.8),
    (data['Rate'] >= 3.8) 
    ]

values = [0, 1, 2]

# create a new column and use np.select to assign values to it using our lists as arguments
data['review'] = np.select(conditions, values)

info = data[['Raters', 'Reviewers', 'Pages', 'PublishYear']]
labels = data.review

classifier = KNeighborsClassifier(n_neighbors = 3)
classifier.fit(info, labels)