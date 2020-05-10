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

def rate_all_trucks(trucks_matrix=rsql("SELECT capacity, fuel_consumption FROM vehicles")):
    ratings = []

    for truck in trucks_matrix:
        ratings.append(dedico.capacity_fuel_coefficient_calculation(truck[0],truck[1]))

    return ratings

def rate_group(dist_or_time_matrix, demand_array):
    tsp_route = tsp.TSP_all_roads(dist_or_time_matrix)
    distance_sum = 0
    previous = 0

    for i in tsp_route:
        distance_sum += dist_or_time_matrix[previous][i]
        previous = i

    rating = dedico.demand_distance_coefficient_calculation(sum(demand_array), distance_sum)

    return rating

def rate_all_groups(*args, demand_array):
    ratings = []

    for i in args:
        ratings.append(rate_group(i, demand_array))

    return ratings


def divide_groups(coordinate_matrix=rsql("SELECT latitude, longitude FROM customers")):
    group_assignment, nr_of_groups = kmeansgroups.get_groups(coordinate_matrix,[2,3,4])
    formatted_coordinates = []
    for i in coordinate_matrix:
        formatted_coordinates.append(str(i[0])+","+str(i[1]))

    # When we are about to try the whole thing live, we uncomment this below, until then, use the line under it
    #distance_matrix, time_matrix = distancematrixtest.produce_matrices(formatted_coordinates)
    distance_matrix, time_matrix = distance, time
    dst_m_exp = pd.DataFrame(distance_matrix)

    # Code below splits distance matrix into the groups given by the k-means
    for i in range(nr_of_groups):
        first_step = pd.DataFrame()
        second_step = pd.DataFrame()
        for idx, j in enumerate(group_assignment):
            if j == i or idx == 0:
                first_step = first_step.append(dst_m_exp.iloc[[idx]])
        for idx, j in enumerate(group_assignment):
            if j == i or idx == 0:
                second_step = second_step.append(first_step[idx])

        second_step.to_pickle(pickle_name+str(i))

    # Uncomment below if you want to see the output of this above
    # for i in range(nr_of_groups):
    #     print("Number: ", i, "\n", pd.read_pickle(pickle_name+str(i)))
    #     print("\n\n")

    # TO DO: Get the demands from customers, split into two parts so they can be sent into the function below
    # rsql("SELECT latitude, longitude FROM customers")
    # ratings = rate_all_groups(pd.read_pickle(pickle_name+str(i)) for i in range(nr_of_groups), )
    print(ratings)
#     return something_later

divide_groups()
# print(divide_groups())


#def demand_distance_coefficient_calculation(demand, distance):
