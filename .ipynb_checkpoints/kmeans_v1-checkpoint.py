import pandas as pd
from sklearn.cluster import KMeans

data = pd.read_csv('ml_data/clustering_data.csv')

info = data[['BookID', 'Author', 'Series', 'Genre']]

#Needs work
def check_authors(authors_1, authors_2):
  distance = 0

  for author in authors_1:
    if author not in authors_2:
      distance += 1
    else:
      distance -= 2

  return distance

def check_tags(tags_1, tags_2):
  distance = 0

  for tag in tags_1:
    if tag not in tags_2:
      distance += 1

  return distance


def distance(book_1, book_2):
  distance = 0

  authors_1 = book_1[0].strip('\"').split(', ')
  authors_2 = book_2[0].strip('\"').split(', ')

  distance += check_authors(authors_1, authors_2)
  distance += check_authors(authors_2, authors_1)

  if book_1[1] != book_2[1]:
    distance += 1

  tags_1 = book_1[2:]
  tags_2 = book_2[2:]

  distance += check_tags(tags_1, tags_2)
  distance += check_tags(tags_2, tags_1)

  return distance if distance > 0 else 0

def isnan(x):
    return x != x

books = info.BookID.unique()
cluster_data = []

for book in books:
  samp = info[info.BookID == book]
  sample_data = []

  series = samp.Series.values[0]
  author = samp.Author.values[0]

  sample_data.append(author)

  if isnan(series):
    sample_data.append('none')
  else:
    sample_data.append(series)

  sample_data += samp.Genre.values.tolist()

  cluster_data.append(sample_data)

while error.all() != 0:
  # Step 2: Assign samples to nearest centroid

  for i in range(len(samples)):
    distances[0] = distance(sepal_length_width[i], centroids[0])
    distances[1] = distance(sepal_length_width[i], centroids[1])
    distances[2] = distance(sepal_length_width[i], centroids[2])
    cluster = np.argmin(distances)
    labels[i] = cluster

  # Step 3: Update centroids

  centroids_old = deepcopy(centroids)

  for i in range(3):
    points = [sepal_length_width[j] for j in range(len(sepal_length_width)) if labels[j] == i]
    centroids[i] = np.mean(points, axis=0)

# Use .fit() to fit the model to samples
model.fit(samples)

# Use .predict() to determine the labels of samples
labels = model.predict(samples) 

print(model.inertia_)