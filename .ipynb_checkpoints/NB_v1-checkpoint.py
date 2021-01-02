import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

data = pd.read_csv('ml_data/classification_data.csv')

info = data[['Raters', 'Reviewers', 'Pages', 'PublishYear']]
labels = data.review

info_train, info_test, labels_train, labels_test = train_test_split(info, labels, train_size = 0.8, test_size = 0.2, random_state=42)

classifier = GaussianNB()
classifier.fit(info_train, labels_train)

predict = classifier.predict(info_test)

test_labels = labels_test.values.tolist()

result_matrix = np.zeros((3, 3), dtype='int32')
correct = 0

for i in range(len(test_labels)):
    result_matrix[test_labels[i]][predict[i]] += 1
    
    if predict[i] == test_labels[i]:
        correct += 1

print(result_matrix)
print(correct/len(test_labels))