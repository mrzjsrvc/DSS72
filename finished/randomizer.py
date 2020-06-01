import pandas as pd
import math
import db

from datetime import datetime
from datetime import timedelta
from db import run_sql_string as rsql

# When testing, use these pre-generated matrices below to avoid sending requests superfluously:
# distance = [[0, 29622, 30337, 31631, 57968], [29010, 0, 32434, 56556, 82894], [30117, 32301, 0, 57663, 84000], [33337, 58184, 58899, 0, 27842], [58811, 83659, 84374, 29970, 0]]
# time = [[0, 1362, 1550, 1585, 2737], [1319, 0, 1577, 2410, 3562], [1549, 1560, 0, 2640, 3792], [1604, 2476, 2663, 0, 1576], [2793, 3665, 3853, 1746, 0]]

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
fuel_price_xx       = 13.5

def datetime_string_to_minutes(date_string):
    res = datetime.strptime(date_string, "%H:%M")
    return (res.hour*60) + (res.minute)

def minutes_to_hours_string(min):
    return str(timedelta(minutes=min))

# If no lunch, set to 00:00, and load_time must make total hours in half of a day evenly divisible(modulus to check)
def plan_random_schedule(distance_matrix, time_matrix, work_start_time=work_start_time_x, work_end_time=work_end_time_x, lunch_time=lunch_time_x, lunch_duration=lunch_duration_x, load_time=load_time_x, unload_time=unload_time_x, break_time=break_time_x, fuel_price_x=fuel_price_xx):
    schedule = []

    start_time_offset = datetime_string_to_minutes(work_start_time)
    lunch_time_start_offset = datetime_string_to_minutes(lunch_time)
    lunch_time_end_offset = lunch_time_start_offset + lunch_duration
    end_time_offset = datetime_string_to_minutes(work_end_time)

    current_time = start_time_offset
    amount_of_intervals = int((end_time_offset - start_time_offset) / load_time)
    # Included amount of intervals within lunch, so the for-loop is easier to generalize

    for i in range(amount_of_intervals):
        if current_time > lunch_time_start_offset and current_time < lunch_time_end_offset: # For workers at the depot
            pass
        else:
            if int(rsql("SELECT SUM(demand) FROM customers;")[0][0]):     # If any demand remains
                update_truck_availability(current_time)                   # MAY NEED TO ADD LUNCH FOR DRIVERS HERE SOMEWHERE
                suggested_route, truck = get_next_truck_group_pair()
                if truck != -1:                                           # If a truck is available #CHANGE: suggested; if truck != -1, and suggested_route != []
                    schedule += single_truck_scheduler(suggested_route[0], truck, current_time, distance_matrix, time_matrix)
            # TAKE THE TRUCK AND SEND IT OFF, PUT AS UNAVAILABLE, SET NEW DEMANDS OF CUSTOMERS
            # WRITE THE ENTIRE SCHEDULE FOR THIS TRUCK FROM START TO FINISH - STORE IT IN "SCHEDULE"
        current_time += load_time

    return schedule

def update_truck_availability(current_time):
    # Doing this solution because otherwise we would have to work on the entire dates as datetime in MySQL, I wanted simple strings, so now we have to use those instead
    unavailable_vehicles = rsql("SELECT vehicles.index, vehicles.return_time FROM vehicles WHERE vehicles.status = 'unavailable'")
    if unavailable_vehicles != "Done":
        for truck in unavailable_vehicles:
            if truck[1] <= current_time:
                rsql("UPDATE vehicles SET vehicles.status = 'available' WHERE vehicles.index = "+str(truck[0]))

def single_truck_scheduler(suggested_route, truck, start_minutes, distance_matrix=None, time_matrix=None, lunch_duration=lunch_duration_x, load_time=load_time_x, unload_time=unload_time_x, break_time=break_time_x, current_location=0, home_depot=0, fuel_price_x=13.5):
    start_timestamp = start_minutes
    departure_timestamp = start_minutes + load_time

    schedule_array = []

    truck_capacity = truck[2]
    currently_carrying = truck_capacity

    fuel_price = truck[3]

    next_distance, next_distance_time = distance_matrix[home_depot][suggested_route], (time_matrix[home_depot][suggested_route] / 60)
    distance_home, distance_home_time = distance_matrix[suggested_route][home_depot], (time_matrix[suggested_route][home_depot] / 60)

    arrival_timestamp = None
    unload_timestamp = None
    break_timestamp = None
    return_timestamp = None

    next_demand = rsql("SELECT customers.demand FROM customers WHERE customers.index = "+str(suggested_route))[0][0]
    print("next_demand: ",next_demand,type(next_demand),"\n\n")

#=====================================================================================================
    arrival_timestamp = departure_timestamp + next_distance_time
    unload_timestamp = arrival_timestamp    # Start unloading immediately upon arrival
    break_timestamp = unload_timestamp + unload_time

    schedule_line = [str(truck[0]), str(current_location), str(suggested_route), str(currently_carrying), minutes_to_hours_string(start_timestamp), minutes_to_hours_string(departure_timestamp), minutes_to_hours_string(arrival_timestamp), minutes_to_hours_string(unload_timestamp), minutes_to_hours_string(break_timestamp), str(next_distance), str(math.ceil(fuel_price_x*(fuel_price/100)*(next_distance/1000)))]
    schedule_array.append(schedule_line)

    start_timestamp = break_timestamp + break_time
    departure_timestamp = start_timestamp

    if next_demand >= currently_carrying:
        next_demand -= currently_carrying
        currently_carrying = 0
    else:
        currently_carrying -= next_demand
        next_demand = 0

    if next_demand == 0:
        rsql("UPDATE customers SET customers.status = 'inactive' WHERE customers.index = "+str(suggested_route))

    rsql("UPDATE customers SET customers.demand = "+str(next_demand)+" WHERE customers.index = "+str(suggested_route))
    current_location = suggested_route

    return_timestamp = break_timestamp + break_time + distance_home_time #CHANGE
#=====================================================================================================

    arrival_timestamp = departure_timestamp + distance_home_time
    unload_timestamp = arrival_timestamp
    break_timestamp = unload_timestamp

    schedule_line = [str(truck[0]), str(current_location), str(home_depot), str(currently_carrying), minutes_to_hours_string(start_timestamp), minutes_to_hours_string(departure_timestamp), minutes_to_hours_string(arrival_timestamp), minutes_to_hours_string(unload_timestamp), minutes_to_hours_string(break_timestamp), str(distance_home), str(math.ceil(fuel_price_x*(fuel_price/100)*(distance_home/1000)))]
    schedule_array.append(schedule_line)

#=====================================================================================================

    rsql("UPDATE vehicles SET vehicles.status = 'unavailable' WHERE vehicles.index = "+str(truck[0]))
    rsql("UPDATE vehicles SET vehicles.return_time = "+str(return_timestamp)+" WHERE vehicles.index = "+str(truck[0]))
    return schedule_array

def get_next_truck_group_pair():

    customer = rsql("SELECT * FROM customers WHERE customers.status = 'active'")
    truck = rsql("SELECT * FROM vehicles WHERE vehicles.status = 'available' LIMIT 1")

    #CHANGE: or customer, or customer
    if truck == "Done" or truck == [] or customer == "Done" or customer == []: # If all trucks are occupied or no more customers left
        return [0], -1
    else:
        return customer[0], truck[0]

# db.init()
# arr = plan_random_schedule()
# print("truck ID, curr_loc, home, curr_carr, start, depart, arrive, unload, break, distance, price")
# for i in arr:
#     print(" ".join(i))
