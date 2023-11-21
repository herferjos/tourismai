import streamlit as st
import pandas as pd
import pydeck as pdk

# Lista de coordenadas de algunas ciudades de España
coordenadas = [
    [36.721261, -4.421266, "Málaga"],
    [37.389092, -5.984459, "Sevilla"],
    [40.416775, -3.703790, "Madrid"],
    [41.385064, 2.173404, "Barcelona"],
    [43.263013, -2.934985, "Bilbao"]
]

# Crear un dataframe con las coordenadas y los nombres de las ciudades
df = pd.DataFrame(coordenadas, columns=["lat", "lon", "nombre"])

# Establecer el estado inicial de la vista del mapa
view_state = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lon"].mean(),
    zoom=5
)

# Crear una capa de marcadores con los nombres de las ciudades
marker_layer = pdk.Layer(
    type="ScatterplotLayer",
    data=df,
    get_position="[lon, lat]",
    get_radius=500,
    get_color=[255, 0, 0],
    pickable=True
)

# Crear una capa de línea que conecta los puntos según el orden de la lista
line_layer = pdk.Layer(
    type="PathLayer",
    data=df,
    get_path="[lon, lat]",
    get_color=[0, 0, 255],
    width_scale=10,
    width_min_pixels=2
)

# Crear un objeto de Deck con las capas y el estado de la vista
deck = pdk.Deck(
    layers=[marker_layer, line_layer],
    initial_view_state=view_state,
    tooltip={"text": "{nombre}"}
)

# Mostrar el mapa en Streamlit
st.pydeck_chart(deck)


# Importar la biblioteca Folium
import folium

# Crear un objeto Map con la ubicación inicial y el nivel de zoom
mapa = folium.Map(location=[40.4167, -3.70325], zoom_start=13)

# Definir los puntos de interés y sus coordenadas
puntos = [
    ("Puerta del Sol", [40.4168, -3.7034]),
    ("Plaza Mayor", [40.4154, -3.7074]),
    ("Palacio Real", [40.4179, -3.7143]),
    ("Templo de Debod", [40.4240, -3.7178]),
    ("Parque del Retiro", [40.4146, -3.6846]),
    ("Museo del Prado", [40.4138, -3.6922])
]

# Añadir los puntos de interés al mapa como marcadores
for punto, coordenadas in puntos:
    folium.Marker(
        location=coordenadas,
        icon=folium.Icon(color="red"),
        popup=punto
    ).add_to(mapa)

# Calcular la ruta óptima entre los puntos de interés
# Aquí se podría usar algún algoritmo como el problema del viajante o el algoritmo de Dijkstra
# Por simplicidad, se asume que la ruta es la misma que el orden de los puntos
ruta = [coordenadas for punto, coordenadas in puntos]

# Añadir la ruta al mapa como una línea
folium.PolyLine(
    locations=ruta,
    color="blue",
    weight=3,
    dash_array="5, 5"
).add_to(mapa)

# Mostrar el mapa en la aplicación de Streamlit
st.folium_static(mapa)
