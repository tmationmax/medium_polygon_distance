from geopy.distance import great_circle as distance
from geopy.point import Point as Point
from math import sin, cos, atan2, sqrt, degrees, radians, pi


def midpoint(a, b):
    a_lat, a_lon = radians(a.latitude), radians(a.longitude)
    b_lat, b_lon = radians(b.latitude), radians(b.longitude)
    delta_lon = b_lon - a_lon
    B_x = cos(b_lat) * cos(delta_lon)
    B_y = cos(b_lat) * sin(delta_lon)
    mid_lat = atan2(
        sin(a_lat) + sin(b_lat),
        sqrt(((cos(a_lat) + B_x) ** 2 + B_y ** 2))
    )
    mid_lon = a_lon + atan2(B_y, cos(a_lat) + B_x)
    # Normalise
    mid_lon = (mid_lon + 3 * pi) % (2 * pi) - pi

    return Point(latitude=degrees(mid_lat), longitude=degrees(mid_lon))

def get_line_midpoint(line):
    a = Point(line[0])
    b = Point(line[1])

    return midpoint(a,b)


def calculate_dist_to_line(line_a_lat, line_a_lng, line_b_lat, line_b_lng, point_object):
    a = Point(latitude=line_a_lat, longitude=line_a_lng)
    b = Point(latitude=line_b_lat, longitude=line_b_lng)
    dist = distance(midpoint(a, b), point_object)
    return dist


def get_min_distance_to_arr(arr_coords, point_object, unit='m'):
    min_dist = 999999
    line=[]
    for i, _ in enumerate(arr_coords):
        if i + 1 < len(arr_coords):
            dist = calculate_dist_to_line(
                line_a_lat=arr_coords[i][1],
                line_a_lng=arr_coords[i][0],
                line_b_lat=arr_coords[i + 1][1],
                line_b_lng=arr_coords[i + 1][0],
                point_object=point_object
            )
            if dist < min_dist:
                min_dist = dist
                line = [(arr_coords[i][1], arr_coords[i][0]), (arr_coords[i + 1][1], arr_coords[i + 1][0])]
        else:
            dist = calculate_dist_to_line(
                line_a_lat=arr_coords[i][1],
                line_a_lng=arr_coords[i][0],
                line_b_lat=arr_coords[0][1],
                line_b_lng=arr_coords[0][0],
                point_object=point_object
            )
            if dist < min_dist:
                min_dist = dist
                line = [(arr_coords[i][1], arr_coords[i][0]), (arr_coords[0][1], arr_coords[0][0])]

    if unit == 'm':
        return min_dist.m, line
    elif unit == 'km':
        return min_dist.km, line
    else:
        return min_dist, line
