import grouper
import router
import pandas as pd
import dedico
import tsp
from db import run_sql_string as rsql

#stuff_1 = grouper.divide_groups()       # Sets ratings and divides groups in database, returns distancce- & time matrix (recycles matrices to avoid more requests to Google)
grouper.rate_all_trucks()     # Sets ratings of all trucks in database

#     group_nr = rsql("SELECT * FROM customers WHERE customers.group = 1 OR customers.depot = 1")
#     truck_index = rsql("SELECT * FROM vehicles WHERE vehicles.index = 1")
#     distance_matrix, time_matrix = grouper.divide_groups()
# # router
#     stuff = router.suggested_full_route(distance_matrix, time_matrix, group_nr, truck_index)
