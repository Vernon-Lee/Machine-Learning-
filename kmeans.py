# import libraries
import numpy as np
import matplotlib.pyplot as plt
import csv
import random


# Define a function that computes the distance between two data points
def euclidean_distance(point1, point2):
    return np.sqrt((point2[1] - point1[1]) ** 2 + (point2[0] - point1[0]) ** 2)


def point_mean(points):
    pointY = 0
    pointX = 0
    for p in points:
        pointX += p[0]
        pointY += p[1]
    return [
        pointX / len(points),
        pointY / len(points),
    ]


# Define a function that finds the closest centroid to each point out of all the centroids
# HINT: This function should call the function you implemented that computes the distance between two data points.
# HINT: Numpy has a useful method that allows you to find the index of the smallest value in an array. 
def closest_centroid(center_points, point_xy):
    closest_center_point = 0
    distance_centroid = euclidean_distance(center_points[0], point_xy)
    for center_point, center in enumerate(center_points):
        distance = euclidean_distance(center, point_xy)
        if distance < distance_centroid:
            distance_centroid = distance
            closest_center_point = center_point
    return closest_center_point


# Write a function to visualise the clusters. (optional, but useful to see the changes and if your algorithm is working)
def build_clusters(center_point, points):
    clusters = [{'center_point': c_point, 'data_points': []} for c_point in center_point]
    for point_xy in points:
        nearest_center_point_idx = closest_centroid(center_point, point_xy)
        clusters[nearest_center_point_idx]['data_points'].append(point_xy)
    return clusters


# Write the initialisation procedure
if __name__ == '__main__':
    country_data = []
    # ====
    # reads data in from the csv files
    with open('dataBoth.csv') as file:
        read_file = csv.reader(file, delimiter=',')
        for row in read_file:
            if row[0] != 'Countries':
                birth = float(row[1])
                life = float(row[2])

                country_data.append([birth, life])
    num_clusters = int(input("Input number of clusters: "))
    num_iterate = int(input("Input amount of iterations: "))
    built_clusters = []
    for i in range(num_iterate):
        iteration_distance = 0.0
        if i == 0:
            centroid = random.sample(country_data, num_clusters)
        else:
            centroid = [point_mean(c['data_points']) for c in built_clusters]
        built_clusters = build_clusters(centroid, country_data)
        for cluster in built_clusters:
            mean = cluster['center_point']
            for point in cluster['data_points']:
                iteration_distance += euclidean_distance(point, mean)
        print(f"Sum of euclidean distances for iteration {i + 1} is {iteration_distance}.")
    figure = plt.figure()
    plt.title('LifeExpectancy and BirthRate')
    plt.ylabel('LifeExpectancy')
    plt.xlabel('BirthRate')
    cluster_count = 1
    country_list = []
    for cluster in built_clusters:
        # give clusters random colours
        r = random.random()
        b = random.random()
        g = random.random()
        color = [[r, g, b]]
        num_countries = 0
        # loop through clusters,
        # calc the average, sums of each cluster
        for point in cluster['data_points']:
            x = point[0]
            y = point[1]
            sum_x = 0
            sum_y = 0
            sum_x += x
            sum_y += y
            # visualise cluster
            plt.scatter(point[0], point[1], c=color)
            num_countries += 1
            # open file to check where in which cluster each country is
            with open('dataBoth.csv') as file:
                read_file = csv.reader(file, delimiter=',')
                for row in read_file:
                    if row[0] != 'Countries' and x == float(row[1]) and y == float(row[2]):
                        country_name = str(row[0])
                        country_list.append(country_name)
        # The number of countries belonging to each cluster
        print(f"\nCluster {cluster_count} contains {num_countries}: countries.")
        # The list of countries belonging to each cluster
        print(f"The list of countries in cluster {cluster_count}: {country_list}")
        # The mean Life Expectancy and Birth Rate for each cluster
        print(f"Cluster {cluster_count} mean birth rate: {sum_x / num_countries}")
        print(f"Cluster {cluster_count} mean life expectancy: {sum_y / num_countries}")
        country_list.clear()
        cluster_count += 1
    # Display cluster graph
    plt.show()
