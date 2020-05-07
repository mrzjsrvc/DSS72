'''
Created on May 1, 2020

@author: matteo
'''
from plotly.io._base_renderers import open_html_in_browser
'''
Created on Apr 29, 2020

@author: matteo
'''

import googlemaps
from datetime import datetime
import json
import webbrowser
import db

with open('./key.txt') as infile:
    g_key = infile.readline()

key_string = "&key="+g_key
base = "https://maps.googleapis.com/maps/api/staticmap?size=1200x1200&center=Blekinge&zoom=9"


def make_coord_string(lat,long):
    return "&markers=color:yellow%7Clabel:S%7C"+str(lat)+","+str(long)


def make_url(poly_url):
    blek_lat = 59.511608
    blek_long = 14.148330
    url = base+make_coord_string(blek_lat, blek_long)
    for p in poly_url:
        url +=p
    return url+key_string


#POLYNAME
def make_poly_string(poly):
    return "&path=weight:4|color:red|enc:"+poly

def poly_corrector(poly_str):
    if(poly_str.find("\\")):
        poly_str.replace("\\", "\"")
    return poly_str


def dir_calculator(coord):
    gmaps = googlemaps.Client(key=g_key)
    directions_result = gmaps.directions(str(coord[0])+","+str(coord[1]),str(coord[2])+","+str(coord[3]),
#                                    waypoints = ["Ronneby"],
                                     mode="driving",
                                     traffic_model = "pessimistic", #just an hypotesis
                                     alternatives = True, #all possible paths
                                     departure_time=datetime.now())
    return directions_result

def poly_extr(directions_result):
    i = 0
    poly_list = []
    while(i < len(directions_result)):
        poly_list.append(directions_result[i].get("overview_polyline"))
        i += 1

    ris = []
    for poly in poly_list:
        poly = poly_corrector(poly["points"])
        ris.append(poly)

    return ris

def distance_extr(leg):
    dist = leg[0].get("distance")
    print(dist.get("text"))

def time_extr(leg):
    time = leg[0].get("duration")
    print(time.get("text"))

def time_with_traffic_extr(leg):
    time = leg[0].get("duration_in_traffic")
    print(time.get("text"))


def legs_extr(directions_result):
    i = 0
    leg = []
    while( i < len(directions_result)):
        leg = directions_result[i].get("legs")
        distance_extr(leg)
        time_extr(leg)
        time_with_traffic_extr(leg)
        i += 1


def coord_extr(loc1,loc2):
    coordinates = []
    lat = db.run_sql_string("SELECT latitude FROM customers WHERE name="+"'"+loc1+"'"+";")
    long = db.run_sql_string("SELECT longitude FROM customers WHERE name="+"'"+loc1+"'"+";")
    lat1 = db.run_sql_string("SELECT latitude FROM customers WHERE name="+"'"+loc2+"'"+";")
    long1 = db.run_sql_string("SELECT longitude FROM customers WHERE name="+"'"+loc2+"'"+";")
    coordinates.append(lat[0][0])
    coordinates.append(long[0][0])
    coordinates.append(lat1[0][0])
    coordinates.append(long1[0][0])
    return coordinates

if __name__ == '__main__':


    loc1 = input("Insert source point")
    loc2 = input("Insert destination point")

    poly_url = []
    coordinates = coord_extr(loc1,loc2)

    #Request real time path with details
    directions = dir_calculator(coordinates)
    #Extract the attribute to plot the path in a map
    poly_ris = poly_extr(directions)
    #Extract details as time,time_in_traffic,distance
    legs_extr(directions)

    #If there are different possible path, display all of them
    for poly in poly_ris:
        poly_url.append(make_poly_string(poly))

    #Build the URL for the map request
    url = make_url(poly_url)
    webbrowser.open(url)
