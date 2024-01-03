import json
import streamlit as st
from modules import get_planning

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

def mostrar_mapa_ubicacion(latitud, longitud):
    iframe = f'<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d3197.081192205956!2d{longitud}!3d{latitud}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1ses!2ses!4v1704301991010!5m2!1ses!2ses" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
    st.markdown(iframe, unsafe_allow_html=True)

def mostrar_ruta_entre_ubicaciones(latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    iframe = f'<iframe src="https://www.google.com/maps/embed?pb=!1m24!1m12!1m3!1d7177.278003338615!2d{longitud_origen}!3d{latitud_origen}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m9!3e6!4m3!3m2!1d{latitud_destino}!2d{longitud_destino}!4m3!3m2!1d{latitud_destino}!2d{longitud_destino}!5e0!3m2!1ses!2ses!4v1704302063485!5m2!1ses!2ses" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
    st.markdown(iframe, unsafe_allow_html=True)

# Coordenadas del Palacio Real en Madrid
latitud_palacio_real = 40.4171
longitud_palacio_real = -3.7138

# Coordenadas del Estadio Santiago Bernabéu
latitud_bernabeu = 40.4530
longitud_bernabeu = -3.6883

# Mostrar la ubicación del Palacio Real
mostrar_mapa_ubicacion(latitud_palacio_real, longitud_palacio_real)

# Mostrar la ruta entre el Palacio Real y el Estadio Santiago Bernabéu
mostrar_ruta_entre_ubicaciones(latitud_palacio_real, longitud_palacio_real, latitud_bernabeu, longitud_bernabeu)



city = st.text_input(label=":blue[City to visit]", placeholder="Escribe tu ciudad...")
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

plan, places, routes = st.tabs(['Planning', 'Information', 'Routes'])



st.write(st.session_state.responses)
st.write(st.session_state.planning)


with plan:
    if 'planning' in st.session_state:
        st.markdown(st.session_state.planning['html_planning'], unsafe_allow_html=True)
with places:

    st.write ("---")

with routes:

    st.write ("---")

    st.write("## Routes")
    for i in range(len(st.session_state.planning['order'])):
        day = st.session_state.planning['order'][i]

        for j in range(len(day) - 1):
            st.markdown(f"_**From {day[j]} To {day[j+1]}**_")
            cord_long_1 = st.session_state.planning['ordered_coordinates'][i][j][0]
            cord_lat_1 = st.session_state.planning['ordered_coordinates'][i][j][1]

            cord_long_2 = st.session_state.planning['ordered_coordinates'][i][j+1][0]
            cord_lat_2 = st.session_state.planning['ordered_coordinates'][i][j+1][1]   

            m = get_map(day, j, cord_long_1, cord_lat_1, cord_long_2, cord_lat_2)
            with st.expander("🗺️ Map"):
                st_folium(m, width=2000)

