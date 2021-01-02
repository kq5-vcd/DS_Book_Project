import pandas as pd
from KModes import KModes
from sklearn.model_selection import train_test_split

data = pd.read_csv('ml_data/clustering_data.csv')

info = data[['BookID', 'Author', 'Series', 'Genre']]

#Needs work
def check_tags(tags_1, tags_2):
  total_length = max(len(tags_1), len(tags_2))
  difference = total_length

  for tag in tags_1:
    if tag in tags_2:
      difference -= 1

  return difference/total_length


def distance(book_1, book_2):
  distance = 0.0

  authors_1 = book_1[0].strip('\"').split(', ')
  authors_2 = book_2[0].strip('\"').split(', ')

  for author in authors_1:
    if author in authors_2:
      break
  else:
    distance += 1

  if book_1[1] != 'none' and book_1[1] == book_2[1]:
    distance += 0
  else:
    distance += 1

  tags_1 = book_1[2:]
  tags_2 = book_2[2:]

  distance += check_tags(tags_1, tags_2)

  return distance

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

def get_frequency(book, cluster):
  authors = book[0].strip('\"').split(', ')

  for author in authors:
    if author in cluster['author']:
      cluster['author'][author] += 1
    else:
      cluster['author'][author] = 1

  if book[1] in cluster['series']:
    cluster['series'][book[1]] += 1
  else:
    cluster['series'][book[1]] = 1

  for tag in book[2:]:
    if tag in cluster['tags']:
      cluster['tags'][tag] += 1
    else:
      cluster['tags'][tag] = 1

  length = len(book)

  if length in cluster['length']:
    cluster['length'][length] += 1
  else:
    cluster['length'][length] = 1

  return cluster

sample_frequency = {'author': {}, 'series': {}, 'tags': {}, 'length': {}}

def get_centroid(cluster):
  new_centroid = []

  new_centroid.append(max(cluster['author'], key = cluster['author'].get))
  new_centroid.append(max(cluster['series'], key = cluster['series'].get))

  tag_len = max(cluster['length'], key = cluster['length'].get) - 2

  tags_sorted = {k: v for k, v in sorted(cluster['tags'].items(), key=lambda item: item[1])}
  tags = [x[0] for x in tags_sorted.items()[:tag_len]]

  new_centroid += tags

  return new_centroid

  
info_train, info_test = train_test_split(cluster_data, train_size = 0.8, test_size = 0.2, random_state=42)

model = KModes(distance, get_frequency, sample_frequency, get_centroid, 5)
model.fit(info_train)

print(model.inertia())