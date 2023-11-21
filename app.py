import folium
from streamlit_folium import st_folium
import openrouteservice
from openrouteservice import convert
import json
import streamlit as st
from modules import get_route


ciudad = st.selectbox("Selecciona la ciudad", ["Madrid", "Barcelona"])

if ciudad == "Madrid":
    coords = {
            'lugares': ['madrid_museo_del_prado', 'madrid_puerta_del_sol', 'madrid_plaza_mayor', 'madrid_el_retiro', 'madrid_palacio_real'],
            'coords': [(-3.6923, 40.41378), (-3.70325, 40.41673), (-3.70742, 40.41536), (-3.68282, 40.41543), (-3.71426, 40.41794)]} 
    centro = [40.4165, -3.70256]
else:
    coords = {
        'lugares': ['barcelona_parque_guell', 'barcelona_sagrada_familia', 'barcelona_casa_batllo', 'barcelona_las_ramblas', 'barcelona_camp_nou'],
        'coords': [(2.1527,41.41449), (2.17435, 41.40363), (2.16477, 41.39164), (2.1677, 41.38096), (2.12282, 41.3809)]}
    centro = [41.38879, 2.15899]

m = folium.Map(location=centro, zoom_start=12, control_scale=True, tiles="cartodbpositron")

for i, lugar in enumerate(coords['lugares']):
    folium.Marker(
        location=coords['coords'][i][::-1],
        popup=lugar,
        icon=folium.Icon(color="green" if ciudad == "Madrid" else "red"),
    ).add_to(m)

for i in range(len(coords['lugares']) - 1):
    route_coords = tuple(coords['coords'][i:i + 2])
    
    route = get_route(route_coords)
    geometry = route['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)
    distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(route['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
    duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(route['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
    
    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=800)).add_to(m)

st_folium(m, width=2000)