from __future__ import division
from __future__ import print_function
import requests
import json
import urllib
import sys

def create_data(coordinates, API_key):
  """Creates the data."""
  data = {}
  data['API_key'] = API_key # key_contents if len(key_contents) else sys.argv[1]
  data['addresses'] = [i[0] for i in coordinates]
  return data

def create_distance_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]
  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses)
  max_rows = max_elements // num_addresses
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []
  time_matrix = []

  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    add_distance_matrix, add_time_matrix = build_distance_matrix(response)
    distance_matrix += add_distance_matrix
    time_matrix += add_time_matrix

  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    add_distance_matrix, add_time_matrix = build_distance_matrix(response)
    distance_matrix += add_distance_matrix
    time_matrix += add_time_matrix

  return distance_matrix, time_matrix

def send_request(origin_addresses, dest_addresses, API_key):
  def build_address_str(addresses):
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = urllib.request.urlopen(request).read()
  response = json.loads(jsonResult)
  return response

def build_distance_matrix(response):
  distance_matrix = []
  time_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
    row_list_time = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
    time_matrix.append(row_list_time)

  return distance_matrix, time_matrix

def produce_matrices(coordinates, API_key):
  data = create_data(coordinates, API_key)
  addresses = data['addresses']
  API_key = data['API_key']
  distance_matrix, time_matrix = create_distance_matrix(data)
  return distance_matrix, time_matrix
