import arcgis.gis
import pandas as pd
import arcgis.features as fts
import arcgis.network as ntw
from arcgis.gis import GIS

usr, pwd, url = (open("key.txt", "r").read()).split(",", 2)
gis_t = GIS("https://www.arcgis.com", username=usr, password=pwd)#username="someuser", password="secret1234")
dir = "./testdata/"

df_orders = pd.read_csv(dir+"orders.txt")
df_depots = pd.read_csv(dir+"depots.txt")
df_routes = pd.read_csv(dir+"routes.txt")
df_breaks = None # pd.read_csv(dir+"breaks.txt")

ofs = fts.FeatureSet.from_dataframe(df_orders)
dfs = fts.FeatureSet.from_dataframe(df_depots)
rfs = fts.FeatureSet.from_dataframe(df_routes)
bfs = None # FeatureSet.from_dataframe(df_breaks)

result = ntw.analysis.solve_vehicle_routing_problem(orders=ofs, depots=dfs, routes=rfs, breaks=bfs, time_units='Minutes', distance_units='Kilometers', analysis_region='Europe', default_date=None, uturn_policy='ALLOW_DEAD_ENDS_ONLY', time_window_factor='High', spatially_cluster_routes=True, route_zones=None, route_renewals=None, order_pairs=None, excess_transit_factor='Medium', point_barriers=None, line_barriers=None, polygon_barriers=None, use_hierarchy_in_analysis=True, restrictions=None, attribute_parameter_values=None, populate_route_lines=True, route_line_simplification_tolerance=None, populate_directions=True, directions_language='en', directions_style_name='NA Desktop', travel_mode='Custom', impedance='Truck Time', gis=gis_t, time_zone_usage_for_time_fields='GEO_LOCAL', save_output_layer=False, overrides=None, save_route_data=False, time_impedance=None, distance_impedance=None, populate_stop_shapes=False, output_format=None, future=False)

print(result)
