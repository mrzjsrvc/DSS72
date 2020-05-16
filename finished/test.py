from pathlib import Path
import distancematrix
from db import run_sql_string as rsql

#coordinates = rsql("SELECT CONCAT(customers.latitude, ',', customers.longitude) FROM customers WHERE customers.status = 'active' OR customers.depot IS TRUE")

# distmx, timemx = distancematrix.produce_matrices(coordinates)
# print(distmx)

# key_path = str(Path(__file__).resolve().parents[2]) + "\\key.txt" # up(up(up(__file__))) + "\\key.txt"
# API_key = (open(key_path, "r").read())
# print(key_path, API_key)
