from db import run_sql_string as rsql
import kmeansgroups
import tsp
# import distancematrixtest
import dedico
# import os
import pandas as pd
import tables

pickle_name = "pickle"

# Use these pre-generated matrices below to avoid sending requests superfluously:
distance = [[0, 29622, 30337, 31631, 57968], [29010, 0, 32434, 56556, 82894], [30117, 32301, 0, 57663, 84000], [33337, 58184, 58899, 0, 27842], [58811, 83659, 84374, 29970, 0]]
time = [[0, 1362, 1550, 1585, 2737], [1319, 0, 1577, 2410, 3562], [1549, 1560, 0, 2640, 3792], [1604, 2476, 2663, 0, 1576], [2793, 3665, 3853, 1746, 0]]

def rate_all_trucks(trucks_matrix=rsql("SELECT vehicles.index, vehicles.capacity, vehicles.fuel_consumption FROM vehicles")):
    ratings = []

    for truck in trucks_matrix:
        ratings.append(dedico.capacity_fuel_coefficient_calculation(truck[1],truck[2]))

    rsql("UPDATE vehicles SET vehicles.rating = -1")
    for index, i in enumerate(ratings):
        rsql("UPDATE vehicles SET vehicles.rating = "+str(i)+" WHERE vehicles.index = "+str(index))

    return ratings

def rate_group(dist_or_time_matrix, demand_array, demand_group):
    tsp_route = tsp.TSP_all_roads(dist_or_time_matrix)  # <- This sh** made me have to do the complicated stuff below
    distance_sum = 0                                    # It didn't keep the indices I sent in, so I have to "remake them" with more data
    previous = 0

    # restore the indices
    processed_tsp_routes = [demand_group[i] for i in tsp_route]

    # print("==========================")
    # print(dist_or_time_matrix)
    for i in processed_tsp_routes:
        distance_sum += dist_or_time_matrix[previous][i]
        previous = i
    rating = dedico.demand_distance_coefficient_calculation(sum(demand_array), distance_sum)

    return rating

def rate_all_groups(pickle_names, demand_array, demand_groups): #x, [0, 40, 10, 25, 15] [[0, 1, 2], [0, 3, 4]]
                    #["filename","filename2"], [40,10,25], [[0,1,2],[0,3,4]]
    ratings = []
    demand_array_copy = list(demand_array).copy()   # necessary because generators (i for i in arr) are called by
                                                    # reference(once used, it might disappear, which it did in this case)

    for idx, i in enumerate(pickle_names):
        ratings.append(rate_group(pd.read_pickle(i), demand_array_copy, demand_groups[idx]))
                                    #pd.DataFrame("filename"), [40,10,25], [0,2,3]

    return ratings

def divide_groups():

    customers_matrix = rsql("SELECT customers.latitude, customers.longitude FROM customers WHERE customers.status = 'active' AND customers.depot IS NULL")

    group_assignment = None
    nr_of_groups = 1
    try:
        group_assignment, nr_of_groups = kmeansgroups.get_groups(customers_matrix, list([i for i in range(len(customers_matrix))])[2:]) #Must be at least 2 customers
    except exceptions or Exception:
        group_assignment = [0]
        nr_of_groups = 1                                                  #If less than 2 customers, set to 1 group

    customers_info = rsql("SELECT customers.index, customers.demand FROM customers WHERE status = 'active' AND depot IS NULL")

    demands = [0]
    identity_array = []
    for i in customers_info:
        identity_array.append(i[0])
        demands.append(i[1])

    rsql("UPDATE customers SET customers.group = -1")
    for index, i in zip(identity_array, group_assignment):
        rsql("UPDATE customers SET customers.group = "+str(i)+" WHERE customers.index = "+str(index))

    # ========================================================================================================

    coordinates = rsql("SELECT CONCAT(customers.latitude, ',', customers.longitude) FROM customers WHERE customers.status = 'active' OR customers.depot IS TRUE")
    # When we are about to try the whole thing live, we uncomment this below, until then, use the line under it
    #distance_matrix, time_matrix = distancematrixtest.produce_matrices(coordinates)
    distance_matrix, time_matrix = distance, time
    dst_m_exp = pd.DataFrame(distance_matrix)

    #print(coordinates)

    demand_matrix = []
    for i in range(nr_of_groups):
        new_demand_group_arr = [0]
        for idx, j in enumerate(group_assignment):
            if i == j:
                new_demand_group_arr.append(idx+1)
        demand_matrix.append(new_demand_group_arr)

    # Code below splits distance matrix into the groups given by the k-means
    pickle_names_arr = []
    for index, i in enumerate(demand_matrix):
        result = dst_m_exp.iloc[i,i]

        temp = pickle_name+str(index)
        pickle_names_arr.append(temp)
        result.to_pickle(temp)
        # print(result)

    # Uncomment below if you want to see the output of this above
    # for i in range(nr_of_groups):
    #     print("Number: ", i, "\n", pd.read_pickle(pickle_name+str(i)))
    #     print("\n\n")

    ratings = rate_all_groups(pickle_names_arr, demands, demand_matrix)
    rsql("DELETE FROM groups")
    for i in ratings:
        rsql("INSERT INTO groups(rating) VALUES ("+str(i)+")")

    return distance_matrix, time_matrix
