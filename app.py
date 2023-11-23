
from streamlit_folium import st_folium
import openrouteservice
from openrouteservice import convert
import json
import streamlit as st
from modules import get_route, get_planning, get_map


st.set_page_config(page_title="TourismAI", page_icon="📌", layout="wide")

st.markdown(
  """
  <div style='text-align: center;'>
      <h1>✈️ TourismAI 📌</h1>
      <h4> Tour AI-powered Assistant</h4>
  </div>
  """,
    unsafe_allow_html=True
)
st.write("---")

city = st.text_input(label=":blue[City to visit]", placeholder="Write here...")
recommendations = st.multiselect(':blue[What do you want to visit?]', ['Restaurants', 'Monuments', 'Art Galleries', 'Museums', 'Pubs', 'Street markets', 'Shopping Centers'])
duration = st.number_input(label=":blue[Nº days]", placeholder="Example: 1 Day Visiting", step = 1)

if duration == 1:
    horas = st.text_input(label=":blue[How much time?]", placeholder="Example: 2 hours of Tour")
else:
    horas = None

extra = st.text_input(label=":blue[Any other suggestions]", placeholder="Write here...")

if st.button(label = "Generate planning tour", type = "primary"):
     with st.spinner("Generating ... ⏳"):
        st.session_state.responses, st.session_state.planning = get_planning(city, recommendations, duration, horas, extra)

if 'planning' in st.session_state:
    st.markdown(st.session_state.planning['html_planning'], unsafe_allow_html=True)

    st.write ("---")

    st.write("## Routes")
    for i in range(len(st.session_state.planning['order'])):
        day = st.session_state.planning['order'][i]

        for j in range(len(day) - 1):
            st.markdown(f"_**From {day[j]} To {day[j+1]}**_")
            with st.expander("🗺️ Map"):
                cord_long_1 = st.session_state.planning['ordered_coordinates'][i][j][0]
                cord_lat_1 = st.session_state.planning['ordered_coordinates'][i][j][1]

                cord_long_2 = st.session_state.planning['ordered_coordinates'][i][j+1][0]
                cord_lat_2 = st.session_state.planning['ordered_coordinates'][i][j+1][1]   

                m = get_map(day, cord_long_1, cord_lat_1, cord_long_2, cord_lat_2)

                st_folium(m, width=2000)

# st.write ("---")

# ciudad = st.selectbox("Selecciona la ciudad", ["Madrid", "Barcelona"])

# if ciudad == "Madrid":
#     coords = {
#             'lugares': ['madrid_museo_del_prado', 'madrid_puerta_del_sol', 'madrid_plaza_mayor', 'madrid_el_retiro', 'madrid_palacio_real'],
#             'coords': [(-3.6923, 40.41378), (-3.70325, 40.41673), (-3.70742, 40.41536), (-3.68282, 40.41543), (-3.71426, 40.41794)]} 
#     centro = [40.4165, -3.70256]
# else:
#     coords = {
#         'lugares': ['barcelona_parque_guell', 'barcelona_sagrada_familia', 'barcelona_casa_batllo', 'barcelona_las_ramblas', 'barcelona_camp_nou'],
#         'coords': [(2.1527,41.41449), (2.17435, 41.40363), (2.16477, 41.39164), (2.1677, 41.38096), (2.12282, 41.3809)]}
#     centro = [41.38879, 2.15899]

# m = folium.Map(location=[coords['coords'][0][1],coords['coords'][0][0]], zoom_start = 16)
# for i, lugar in enumerate(coords['lugares']):
#     folium.Marker(
#         location=coords['coords'][i][::-1],
#         popup=lugar,
#         icon=folium.Icon(color="green" if ciudad == "Madrid" else "red"),
#     ).add_to(m)

# for i in range(len(coords['lugares']) - 1):
#     route_coords = tuple(coords['coords'][i:i + 2])
    
#     route = get_route(route_coords)
#     geometry = route['routes'][0]['geometry']
#     decoded = convert.decode_polyline(geometry)
#     distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(route['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
#     duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(route['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
    
#     folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=800)).add_to(m)

# st_folium(m, width=2000)