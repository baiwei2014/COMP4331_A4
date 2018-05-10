import csv
import scipy.spatial

# function reads in the csv and transforms the data into a dataframe. the data frame is than returned.
def data():
    # initializes the list
    data = []

    # opens the file and reads in all the values
    with open('click-stream event.csv') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONE)
        # skip the first row (headers)
        next(reader, None)
        for row in reader:
            elem = []
            for i in range(1,len(row)):
                elem.append(float(row[i]))
            data.append(elem)

    return data

# function for calculating manhattan distance
def manhattan(db):

    distance_matrix = []
    for k in range(0, len(db)):
        distances = []
        for i in range(0, len(db)):
            distance = 0
            for j in range(0,len(db[0])):
                distance += abs(db[k][j]-db[i][j])
            distances.append(distance)
        distance_matrix.append(distances)
    return distance_matrix

# function for calculating euclidean distance
def euclidean(db):
    distance_matrix = []
    for k in range(0, len(db)):
        distances = []
        for i in range(0, len(db)):
            distance = scipy.spatial.distance.pdist([db[k],db[i]], 'euclidean')
            distances.append(distance)
        distance_matrix.append(distances)
    return distance_matrix

# gets the distance of the k nearest neighbor
def k_distance(k,distance):
    k_distances = [0]*len(distance)
    for i in range(0,len(distance)):
        distance_i = distance[i]
        sorted_distance = sorted(distance_i)
        k_distances[i] = sorted_distance[k]

    return k_distances

# gets a list of all the neighbors within k distance
def k_neighbor(k_dist,distance):
    k_neighbors = []
    for i in range(0,len(distance)):
        neighbors = []
        for j in range(0, len(distance)):
            if (distance[i][j] <= k_dist[i] and not(j == i)):
                neighbors.append(j)
        k_neighbors.append(neighbors)
    return k_neighbors

# finds the lrd for each point
def lrd_o(distance,neighbors,k_dist):
    local_reachability_density = [0]*len(distance)
    reach_distance = [0]*len(distance)
    for i in range(0,len(distance)):
        for j in range(0, len(neighbors[i])):
            if (distance[i][neighbors[i][j]] >= k_dist[neighbors[i][j]]):
                reach_distance[i] += distance[i][neighbors[i][j]]
            else:
                reach_distance[i] +=  k_dist[neighbors[i][j]]
        if (reach_distance[i]==0):
            continue
        else:
            local_reachability_density[i] = len(neighbors[i])/reach_distance[i]
    return local_reachability_density, reach_distance

# LOF implementation
def LOF(k,distance_type,db):
    # create an empty list that will hold the LOF values
    factor = []

    # check for which distance type to use
    # creates a 2D array where the two indexes are the ID's of each point and the value is the distance between them
    if(distance_type == manhattan):
        distance = manhattan(db)
    else:
        distance = euclidean(db)

    # gets the k_distance for each point
    k_dist = k_distance(k,distance)
    # finds the number of neighbors within k_distance for each point
    neighbors = k_neighbor(k_dist,distance)

    # find the lrd and reach distances for each point
    lrd_k, reach_distance = lrd_o(distance,neighbors,k_dist)

    # calculates the LOF for each point
    for i in range(0,len(db)):
        lrd = 0
        for j in neighbors[i]:
            lrd += lrd_k[j]
        factor.append([i,(lrd * reach_distance[i])/(k_dist[i]**2)])

    # returns a list of tuples containing ID and LOF pairs.
    return factor

# helper function for the top_five function
def takeSecond(elem):
    return elem[1]

# takes a list and sorts the results in descending order base on the second element in each tuple
def top_five(outliers):
    outliers.sort(key = takeSecond,reverse = True)
    top_five_outliers = [outliers[:5]]
    return top_five_outliers

if __name__ == "__main__":
    db = data()

    lof1 = LOF(2, manhattan, db)
    lof2 = LOF(3, euclidean, db)

    print top_five(lof1)
    print top_five(lof2)
