import folium
from folium.features import DivIcon
import geojson
from geopy.point import Point

import func_util as fu

with open('arrondissements.geojson') as f:
    data = geojson.loads(f.read())

# Set your point of interest. In our case that is Notre Dame.
poi_name = 'Notre Dam'
poi = [48.864716, 2.349014]

m = folium.Map(location=poi, zoom_start=12, tiles='cartodbpositron')
# Display Arrondissements
folium.GeoJson(data).add_to(m)
# Display Arrondissements Numbers
for arrond in data['features']:
    loc = arrond['properties']['geom_x_y']
    nr = arrond['properties']['c_ar']
    folium.map.Marker(location=loc, icon=DivIcon(
        icon_size=(150, 36),
        icon_anchor=(0, 0),
        html='<div style="font-size: 15pt; color:rgb(41,111,255)">{}</div>'.format(str(nr))
    )).add_to(m)

# Display POI
folium.CircleMarker(location=poi, color='red', radius=5, fill='red').add_to(m)
# Display POI Name
folium.map.Marker(location=poi, icon=DivIcon(
    icon_size=(150, 36),
    icon_anchor=(0, 0),
    html='<div style="font-size: 18pt; color: red">{}</div>'.format(poi_name)
)).add_to(m)

m.save('map_1.html')

# Example with Arrondissement 20
coords = [x['geometry']['coordinates'][0] for x in data['features'] if x['properties']['c_ar'] == 20][0]
p = Point(latitude=poi[0],longitude=poi[1])
dist, line = fu.get_min_distance_to_arr(arr_coords=coords,point_object=p)
line_midpoint = fu.get_line_midpoint(line)

# Map it!
m = folium.Map(location=poi, zoom_start=12, tiles='cartodbpositron')

# Display POI
folium.CircleMarker(location=poi, color='red', radius=5, fill='red').add_to(m)
# Display POI Name
folium.map.Marker(location=poi, icon=DivIcon(
    icon_size=(150, 36),
    icon_anchor=(0, 0),
    html='<div style="font-size: 18pt; color: red">{}</div>'.format(poi_name)
)).add_to(m)

for i, _ in enumerate(coords):
    if i+1 < len(coords):
        folium.PolyLine(locations=[(coords[i][1],coords[i][0]),(coords[i+1][1],coords[i+1][0])], color='blue').add_to(m)
    else:
        folium.PolyLine(locations=[(coords[i][1], coords[i][0]), (coords[0][1], coords[0][0])],
                        color='blue').add_to(m)

folium.PolyLine(locations=line, color='red').add_to(m)
folium.PolyLine(locations=[poi,[line_midpoint.latitude,line_midpoint.longitude]], color='red').add_to(m)
folium.CircleMarker(location=[line_midpoint.latitude,line_midpoint.longitude], color='red', radius=5, fill='red').add_to(m)

new_line_mp = fu.get_line_midpoint([poi,[line_midpoint.latitude,line_midpoint.longitude]])
folium.map.Marker(location=[new_line_mp.latitude,new_line_mp.longitude], icon=DivIcon(
    icon_size=(150, 36),
    icon_anchor=(0, 0),
    html='<div style="font-size: 10pt; color: red">Distance: {} Meters</div>'.format(round(dist))
)).add_to(m)

m.save('map_2.html')

# Map all!
m = folium.Map(location=poi, zoom_start=12, tiles='cartodbpositron')

# Display POI
folium.CircleMarker(location=poi, color='red', radius=5, fill='red').add_to(m)
# Display POI Name
folium.map.Marker(location=poi, icon=DivIcon(
    icon_size=(150, 36),
    icon_anchor=(0, 0),
    html='<div style="font-size: 18pt; color: red">{}</div>'.format(poi_name)
)).add_to(m)

# Display Arrondissements
folium.GeoJson(data).add_to(m)
# Display Arrondissements Numbers
for arrond in data['features']:
    loc = arrond['properties']['geom_x_y']
    nr = arrond['properties']['c_ar']
    folium.map.Marker(location=loc, icon=DivIcon(
        icon_size=(150, 36),
        icon_anchor=(0, 0),
        html='<div style="font-size: 15pt; color:rgb(41,111,255)">{}</div>'.format(str(nr))
    )).add_to(m)

for arrond in data['features']:

    coords = arrond['geometry']['coordinates'][0]
    p = Point(latitude=poi[0],longitude=poi[1])
    dist, line = fu.get_min_distance_to_arr(arr_coords=coords,point_object=p)
    line_midpoint = fu.get_line_midpoint(line)

    # for i, _ in enumerate(coords):
    #     if i+1 < len(coords):
    #         folium.PolyLine(locations=[(coords[i][1],coords[i][0]),(coords[i+1][1],coords[i+1][0])], color='blue').add_to(m)
    #     else:
    #         folium.PolyLine(locations=[(coords[i][1], coords[i][0]), (coords[0][1], coords[0][0])],
    #                         color='blue').add_to(m)

    folium.PolyLine(locations=line, color='red').add_to(m)
    folium.PolyLine(locations=[poi,[line_midpoint.latitude,line_midpoint.longitude]], color='red').add_to(m)
    folium.CircleMarker(location=[line_midpoint.latitude,line_midpoint.longitude], color='red', radius=5, fill='red').add_to(m)

    new_line_mp = fu.get_line_midpoint([poi,[line_midpoint.latitude,line_midpoint.longitude]])
    folium.map.Marker(location=[line_midpoint.latitude,line_midpoint.longitude], icon=DivIcon(
        icon_size=(150, 36),
        icon_anchor=(0, 0),
        html='<div style="font-size: 10pt; color: red">Distance: {} Meters</div>'.format(round(dist))
    )).add_to(m)

m.save('map_3.html')