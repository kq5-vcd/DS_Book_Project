import random
import numpy as np
from copy import deepcopy

class KModes:
    def __init__(self, distance, frequency_calculator, sample_frequency, get_centroid, k):
        self.k = k
        self.distance = distance
        self.frequency_calculator = frequency_calculator
        self.sample_frequency = sample_frequency
        self.get_centroid = get_centroid

    def fit(self, data):
        # Step 1: Get centroids
        self.centroids = []
        centroids_old = []

        for i in range(self.k):
            centroid = random.choice(data)

            while centroid in self.centroids:
                centroid = random.choice(data)

            self.centroids.append(centroid)

        error = np.zeros(self.k)
        labels = [0 for x in range(len(data))]

        while error.all() != 0:
            # Step 2: Distance
            # Cluster labels for each point
            labels = np.zeros(len(data))

            # Distances to each centroid
            distances = np.zeros(self.k)

            # Frequncy for mode
            frequency = [deepcopy(self.sample_frequency) for x in range(self.k)]

            # Calculate distance to each centroid
            for i in range(len(data)):
                for j in range(self.k):
                    distances[j] = self.distance(data[i], self.centroids[j])

                cluster = np.argmin(distances)
                labels[i] = cluster

                frequency[cluster] = self.frequency_calculator(data[i], frequency[cluster])

            # Step 3: Update centroids
            centroids_old = deepcopy(self.centroids)

            for i in range(self.k):
                self.centroids[i] = self.get_centroid(frequency[i])

                error[i] = self.distance(self.centroids[i], centroids_old[i])

        self.set_clusters(data, labels)

    def set_clusters(self, data, labels):
        self.clusters = [[] for x in range(self.k)]
        for i in range(len(data)):
            self.clusters[labels[i]].append(data[i])

    def inertia(self):
        total_distance = 0.0

        for i in range(self.k):
            cluster_distance = 0.0

            for sample in self.clusters[i]:
                cluster_distance += self.distance(self.centroids[i], sample)
            
            total_distance += cluster_distance/len(self.clusters[i])

        return total_distance/(sum(len(x) for x in self.clusters))