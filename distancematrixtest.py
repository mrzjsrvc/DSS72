from __future__ import division
from __future__ import print_function
import requests
import json
import urllib
import sys
import os

key_path = os.path.dirname(os.getcwd()) + "\\key.txt"
key_contents = (open(key_path, "r").read())

def create_data():
  """Creates the data."""
  data = {}
  data['API_key'] = key_contents if len(key_contents) else sys.argv[1]
  data['addresses'] = ["Drottninggatan+57+374+36+Karlshamn", # Depot
                        "Sodergatan+4+294+31+Solvesborg",
                        "Adalsvagen+4+293+34+Olofstrom",
                        "Karlskronagatan+11+372+30+Ronneby",
                        "Norra+Kungsgatan+8+371+33+Karlskrona"
                      ]
  print("create_data\n",data,"\n")
  return data

def create_distance_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]
  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses) # 16 in this example.
  # Maximum number of rows that can be computed per request (6 in this example).
  max_rows = max_elements // num_addresses
  # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []
  # Send q requests, returning max_rows rows per request.
  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)

  # Get the remaining remaining r rows, if necessary.
  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
    print("create_distance_matrix\n",distance_matrix,"\n")
  return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    print("build_address_str\n",address_str,"\n")
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = urllib.request.urlopen(request).read()
  response = json.loads(jsonResult)
  print("send_request\n",response,"\n")
  return response

def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  print("build_distance_matrix:\n",distance_matrix,"\n")
  return distance_matrix

########
# Main #
########
def main():
  """Entry point of the program"""
  # Create the data.
  data = create_data()
  addresses = data['addresses']
  API_key = data['API_key']
  distance_matrix = create_distance_matrix(data)
  print(distance_matrix)
if __name__ == '__main__':
  main()
