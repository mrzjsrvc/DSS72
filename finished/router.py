import grouper
import pandas as pd
import dedico
import tsp
from db import run_sql_string as rsql

def customer_heuristic_rating(distance_matrix, group_nr):

    heuristic_table = []

    customers = [i[0] for i in group_nr]
    result = pd.DataFrame(distance_matrix).iloc[customers,customers]

    heuristic_table.append([9999, 0]) # Add the depot
    offset = 1
    for idx, i in enumerate(customers[offset:]):
        index = group_nr[idx+offset][0]
        demand = group_nr[idx+offset][4]
        distance = distance_matrix[0][i]

        heuristic_table.append([dedico.demand_distance_coefficient_calculation(demand, distance), index])

    # _x = changed / altered
    smallest_value_heuristic = min(heuristic_table)
    heuristic_table = [[i[0] - smallest_value_heuristic[0], i[1]] for i in heuristic_table]

    return heuristic_table

def translate(clist, sought):

    for idx, i in enumerate(clist):
        if i == sought:
            return idx
    return -1

def suggested_full_route(distance_matrix, time_matrix, group_nr):
    if group_nr == "Done":
        return [0]
    else:
        customers = [i[0] for i in group_nr]
        group_distance_matrix = pd.DataFrame(distance_matrix).iloc[customers,customers]

        heuristics_table = customer_heuristic_rating(distance_matrix, group_nr)          # Produce the heuristics table
        goal = min(heuristics_table)[1]                                                  # Index of the location in the SQL table
        start = heuristics_table[0][1]                                                   # Index of the depot in the SQL table

        translated_goal = translate(customers, goal)
        translated_start = translate(customers, start)

        return_path = tsp.TSP_specific_start_to_end(group_distance_matrix, [translated_goal], [translated_start])

        full_path = [customers[i] for i in return_path]

        return full_path

#print(suggested_full_route())

# TO DO:
# Later this should be extended to calculate whether the
# logarithmic proximity of nearest other locations are close enough
# if there is remaining load in the truck so it can judge whether it should go there or return home
# ALSO; the TSP's results need to be tested and verified, it isn't 100% certain that it produces the correct
# calculation, it may have to be tweaked in tsp.py
