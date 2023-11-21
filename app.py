# import streamlit as st
# import pandas as pd
# import pydeck as pdk

# # Lista de coordenadas de algunas ciudades de España
# coordenadas = [
#     [36.721261, -4.421266, "Málaga"],
#     [37.389092, -5.984459, "Sevilla"],
#     [40.416775, -3.703790, "Madrid"],
#     [41.385064, 2.173404, "Barcelona"],
#     [43.263013, -2.934985, "Bilbao"]
# ]

# # Crear un dataframe con las coordenadas y los nombres de las ciudades
# df = pd.DataFrame(coordenadas, columns=["lat", "lon", "nombre"])

# # Establecer el estado inicial de la vista del mapa
# view_state = pdk.ViewState(
#     latitude=df["lat"].mean(),
#     longitude=df["lon"].mean(),
#     zoom=5
# )

# # Crear una capa de marcadores con los nombres de las ciudades
# marker_layer = pdk.Layer(
#     type="ScatterplotLayer",
#     data=df,
#     get_position="[lon, lat]",
#     get_radius=500,
#     get_color=[255, 0, 0],
#     pickable=True
# )

# # Crear una capa de línea que conecta los puntos según el orden de la lista
# line_layer = pdk.Layer(
#     type="PathLayer",
#     data=df,
#     get_path="[lon, lat]",
#     get_color=[0, 0, 255],
#     width_scale=10,
#     width_min_pixels=2
# )

# # Crear un objeto de Deck con las capas y el estado de la vista
# deck = pdk.Deck(
#     layers=[marker_layer, line_layer],
#     initial_view_state=view_state,
#     tooltip={"text": "{nombre}"}
# )

# # Mostrar el mapa en Streamlit
# st.pydeck_chart(deck)

import folium
from streamlit_folium import st_folium
import openrouteservice
from openrouteservice import convert
import json

client = openrouteservice.Client(key='5b3ce3597851110001cf6248c946bd142d614eb5ae23bc126f3e9164')


coords = ((80.21787585263182,6.025423265401452),(80.23990263756545,6.018498276842677))
res = client.directions(coords)
geometry = client.directions(coords)['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

m = folium.Map(location=[6.074834613830474, 80.25749815575348],zoom_start=1000, control_scale=True,tiles="cartodbpositron")
folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(m)

folium.Marker(
    location=list(coords[0][::-1]),
    popup="Galle fort",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=list(coords[1][::-1]),
    popup="Jungle beach",
    icon=folium.Icon(color="red"),
).add_to(m)


st_folium(m, width = 2000)

# import folium
# from streamlit_folium import st_folium
# import openrouteservice

# # Crear un objeto Client con la clave de API
# client = openrouteservice.Client(key='5b3ce3597851110001cf6248c946bd142d614eb5ae23bc126f3e9164')

# # Definir los puntos de interés y sus coordenadas
# puntos = [
#     ("Puerta del Sol", [40.4168, -3.7034]),
#     ("Plaza Mayor", [40.4154, -3.7074]),
#     ("Palacio Real", [40.4179, -3.7143]),
#     ("Templo de Debod", [40.4240, -3.7178]),
#     ("Parque del Retiro", [40.4146, -3.6846]),
#     ("Museo del Prado", [40.4138, -3.6922])
# ]

# # Obtener la ruta óptima entre los puntos de interés usando el método directions
# ruta = client.directions(
#     coordinates=[coordenadas for punto, coordenadas in puntos],
#     profile='foot-walking',
#     optimize_waypoints=True
# )

# # Decodificar la geometría de la ruta a un objeto GeoJSON
# geometria = ruta['routes'][0]['geometry']
# geometria = openrouteservice.convert.decode_polyline(geometria)

# # Crear un objeto Map con la ubicación inicial y el nivel de zoom
# mapa = folium.Map(location=[40.4167, -3.70325], zoom_start=13)

# # Añadir los puntos de interés al mapa como marcadores
# for punto, coordenadas in puntos:
#     folium.Marker(
#         location=coordenadas,
#         icon=folium.Icon(color="red"),
#         popup=punto
#     ).add_to(mapa)

# # Añadir la ruta al mapa como una línea
# folium.PolyLine(
#     locations=geometria['coordinates'],
#     color="blue",
#     weight=3,
#     dash_array="5, 5"
# ).add_to(mapa)

# # Mostrar el mapa en la aplicación de Streamlit
# st_folium(mapa)
