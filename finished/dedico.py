# as much delivered for the least distance; delivered/meters
# 			high delivered/meters value should be given to trucks that have most fuel consumption and least capacity
# 			low delivered/meters value should be given to trucks that have least fuel consumption and most capacity
# pick from available truck in pool
#
# how is the pool updated? does time pass in loops?
#
# after each dispatched truck, recalculate the coefficient to see what the situation is like
# each "round", after one truck has been sent and next is loading, send out "best coeff truck" to "worst coeff location"

def demand_distance_coefficient_calculation(demand, distance):
	return demand / (distance/1000) # 1000 m, converting to km

def capacity_fuel_coefficient_calculation(capacity, fuel_consumption):
	return capacity / fuel_consumption
