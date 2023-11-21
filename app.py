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
