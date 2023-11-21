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
        'coords': [(40.41378, -3.6923), (40.41673, -3.70325), (40.41536, -3.70742), (40.41543, -3.68422), (40.41794, -3.71426)]}
    centro = [40.4165, -3.70256]
else:
    coords = {
        'lugares': ['barcelona_parque_guell', 'barcelona_sagrada_familia', 'barcelona_casa_batllo', 'barcelona_las_ramblas', 'barcelona_camp_nou'],
        'coords': [(41.41449, 2.1527), (41.40363, 2.17435), (41.39164, 2.16477), (41.38096, 2.1677), (41.3809, 2.12282)]}
    centro = [41.40338, 2.17403]

m = folium.Map(location=centro, zoom_start=14, control_scale=True, tiles="cartodbpositron")

for i, lugar in enumerate(coords['lugares']):
    folium.Marker(
        location=coords['coords'][i][::-1],
        popup=lugar,
        icon=folium.Icon(color="green" if ciudad == "Madrid" else "red"),
    ).add_to(m)

for i in range(len(coords['lugares']) - 1):
    route_coords = tuple(coords['coords'][i:i + 2])
    
    # Llama a tu función get_route con el formato correcto
    route = get_route(route_coords)

    # Puedes ajustar esta parte según el formato real de tus resultados
    decoded = route['geometry']
    
    distance_txt = f"<h4><b>Distancia: {round(route['distance'] / 1000, 1)} Km</b></h4>"
    duration_txt = f"<h4><b>Duración: {round(route['duration'] / 60, 1)} Minutos</b></h4>"
    
    folium.PolyLine(decoded, color="blue", weight=2.5, opacity=1).add_to(m)
    folium.Marker(location=route_coords[1][::-1], popup=distance_txt + duration_txt, icon=None).add_to(m)

st_folium(m, width=2000)