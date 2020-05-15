import grouper
import router
import pandas as pd
import dedico
import tsp
import math

from datetime import datetime
from datetime import timedelta
from db import run_sql_string as rsql

# Use these pre-generated matrices below to avoid sending requests superfluously:
distance = [[0, 29622, 30337, 31631, 57968], [29010, 0, 32434, 56556, 82894], [30117, 32301, 0, 57663, 84000], [33337, 58184, 58899, 0, 27842], [58811, 83659, 84374, 29970, 0]]
time = [[0, 1362, 1550, 1585, 2737], [1319, 0, 1577, 2410, 3562], [1549, 1560, 0, 2640, 3792], [1604, 2476, 2663, 0, 1576], [2793, 3665, 3853, 1746, 0]]



# THESE VALUES BELOW ARE EXAMPLE VALUES, NOT HARDCODING
# THE FUNCTIONS CAN TAKE SPECIFIED ARGUMENTS, BUT DURING THE PRESENTATION, THESE ARE HERE
# TO MAKE IT EASIER TO TWEAK THE EXAMPLES DURING THE DEMONSTRATION
lunch_time_x        = "12:00"
lunch_duration_x    = 60
load_time_x         = 15
unload_time_x       = 10
break_time_x        = 10
work_start_time_x   = "08:00"
work_end_time_x     = "17:00"

def datetime_string_to_minutes(date_string):
    res = datetime.strptime(date_string, "%H:%M")
    return (res.hour*60) + (res.minute)

def minutes_to_hours_string(minutes):
    return str(timedelta(minutes=value))

# If no lunch, set to 00:00, and load_time must make total hours in half of a day evenly divisible(modulus to check)
def plan_schedule(work_start_time=work_start_time_x, work_end_time=work_end_time_x, lunch_time=lunch_time_x, lunch_duration=lunch_duration_x, load_time=load_time_x, unload_time=unload_time_x, break_time=break_time_x):
    schedule = []

    start_time_offset = datetime_string_to_minutes(work_start_time)
    lunch_time_start_offset = datetime_string_to_minutes(lunch_time)
    lunch_time_end_offset = lunch_time_start_offset + lunch_duration
    end_time_offset = datetime_string_to_minutes(work_end_time)

    current_time = start_time_offset
    amount_of_intervals = (end_time_offset - start_time_offset) / load_time
    # Included amount of intervals within lunch, so the for-loop is easier to generalize

    grouper.rate_all_trucks()                                                                # Sets ratings of all trucks in database
    distance_matrix, time_matrix = grouper.divide_groups()       # Sets ratings and divides groups in database, returns distance- & time matrix (recycles matrices to avoid more requests to Google)

    for i in range(amount_of_intervals):
        if current_time > lunch_time_start_offset and current_time < lunch_time_end_offset: # For workers at the depot
            pass
        else:
            if int(rsql("SELECT SUM(demand) FROM customers;")[0][0]):     # If any demand remains
                suggested_route, truck = get_next_truck_group_pair()
                if truck != -1:                                           # If a truck is available
                    single_truck_scheduler(suggested_route, truck, current_time, distance_matrix, time_matrix)
            # TAKE THE TRUCK AND SEND IT OFF, PUT AS UNAVAILABLE, SET NEW DEMANDS OF CUSTOMERS
            # WRITE THE ENTIRE SCHEDULE FOR THIS TRUCK FROM START TO FINISH - STORE IT IN "SCHEDULE"
        current_time += load_time


    the_time = datetime.time(6,30)
    value = the_time.hour + the_time.minute/60.0













def single_truck_scheduler(suggested_route, truck, start_minutes, distance_matrix=None, time_matrix=None, lunch_duration=lunch_duration_x, load_time=load_time_x, unload_time=unload_time_x, break_time=break_time_x, current_location=0, home_depot=0):
    distance_matrix, time_matrix = grouper.divide_groups(distance_matrix, time_matrix) # Must be done each time - live changes in demand
    start = minutes_to_hours_string(start_minutes)
    departure = minutes_to_hours_string(start_minutes + load_time)

    arrivals = []
    unloads = []

    truck_capacity = truck[2]
    currently_carrying = truck_capacity

    for next_location in suggested_route:
        next_distance, next_distance_time = distance_matrix[current_location][next_location], time_matrix[current_location][next_location]
        distance_home, distance_home_time = distance_matrix[current_location][home_depot], time_matrix[current_location][home_depot]
        distance_home_to_next, distance_home_to_next_time = distance_matrix[home_depot][next_location], time_matrix[home_depot][next_location]
        distance_next_to_home, distance_next_to_home_time = distance_matrix[next_location][home_depot], time_matrix[next_location][home_depot]

        next_demand = rsql("SELECT customers.demand FROM customers WHERE customers.index = "+str(next_location))[0][0]
        rounds_necessary = math.ceil(next_demand / truck_capacity)
        rounds_necessary_remainder_removed = math.ceil((next_demand - currently_carrying) / truck_capacity)

        if ((rounds_necessary * distance_home_to_next) + distance_home) > ((rounds_necessary_remainder_removed * distance_home_to_next) + next_distance + distance_next_to_home):
            continue # = does remainder of loop, break = skips remainder of loop
        else:



    # for i in suggested_route:
    #
    #
    #
    #
    # next_stop = suggested_route[0]
    #
    # while next_stop != home_depot: # Ahahah, strap on your seatbelts, we're going to Costco next
    #


    # CHECK AFTER EACH STEP; is distance to next >= distance from depot to current?
    # If so, skip route, go back directly
    # OR: if fulfilling next stop's demand in total is more meters than "swinging by" and shipping remainder
    #     then swing by, else return to base to resupply


def get_next_truck_group_pair(distance_matrix=distance, time_matrix=time):
    group_nr = rsql("SELECT * FROM customers WHERE customers.group = (SELECT groups.id FROM groups ORDER BY groups.rating DESC LIMIT 1) OR customers.depot = 1")
    truck = rsql("SELECT * FROM vehicles WHERE vehicles.status = 'available' ORDER BY vehicles.rating DESC LIMIT 1")[0]
    suggested_route = router.suggested_full_route(distance_matrix, time_matrix, group_nr)
    if truck == "Done": # If all trucks are occupied
        return [0], -1
    else:
        return suggested_route, truck

print(get_next_truck_group_pair())
