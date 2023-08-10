#!/usr/bin/env python

import sys
import json
import csv

def convert_point(coordinates):
    return f"POINT({' '.join(map(str, coordinates))})"

def convert_line_string(coordinates):
    points = ', '.join([' '.join(map(str, coord)) for coord in coordinates])
    return f"LINESTRING({points})"

def convert_polygon(coordinates):
    rings_wkt = [f"({' ,'.join([' '.join(map(str, coord)) for coord in ring])})" for ring in coordinates]
    return f"POLYGON({', '.join(rings_wkt)})"

def convert_multi_line_string(coordinates):
    lines = [f"({' ,'.join([' '.join(map(str, coord)) for coord in line])})" for line in coordinates]
    return f"MULTILINESTRING({', '.join(lines)})"

def convert_multi_polygon(coordinates):
    polygons = [f"({' ,'.join([' '.join(map(str, coord)) for coord in ring])})" for polygon in coordinates for ring in polygon]
    return f"MULTIPOLYGON({', '.join(polygons)})"

def convert_geojson_to_geowkt(geojson_geometry):
    if geojson_geometry is None:
        return None

    geometry_type = geojson_geometry.get('type')
    coordinates = geojson_geometry.get('coordinates')
    
    if geometry_type == 'Point':
        return convert_point(coordinates)
    elif geometry_type == 'LineString':
        return convert_line_string(coordinates)
    elif geometry_type == 'Polygon':
        return convert_polygon(coordinates)
    elif geometry_type == 'MultiLineString':
        return convert_multi_line_string(coordinates)
    elif geometry_type == 'MultiPolygon':
        return convert_multi_polygon(coordinates)
    else:
        raise ValueError(f"Unsupported GeoJSON geometry type: {geometry_type}")


def escape_nullish(value):
    return value if value is not None else ""

def convert_json_to_csv(data):
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("Input data should be a non-empty list.")
    
    keys = data[0].keys()
    header = ','.join(keys)
    rows = []
    
    for row in data:
        row_values = [f'"{escape_nullish(row[key])}"' for key in keys]
        rows.append(','.join(row_values))
    
    return header + '\n' + '\n'.join(rows)

if len(sys.argv) < 3:
    print("Please provide a file name and an output file name as command line arguments.")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

if not input_file.endswith((".geojson", ".json")):
    print("File is not a geojson.")
    sys.exit(1)

try:
    with open(input_file, 'r', encoding="utf-8") as f:
        geojson_data = json.load(f)
except FileNotFoundError:
    print("File does not exist.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Invalid GeoJSON format.")
    sys.exit(1)

if 'features' not in geojson_data:
    print("File is not a valid GeoJSON.")
    sys.exit(1)

features = geojson_data['features']
new_json = []

for feature in features:
    properties = feature['properties']
    geowkt = convert_geojson_to_geowkt(feature['geometry']) if 'geometry' in feature else None
    new_feature = {**properties, 'geowkt': geowkt} if geowkt else properties
    new_json.append(new_feature)

new_csv = convert_json_to_csv(new_json)

with open(output_file, 'w', encoding="utf-8", newline='') as f:
    f.write(new_csv)

print("File written successfully.")
