import json
import streamlit as st
from modules import get_planning, generar_iframe_ruta, generar_iframe_ubicacion

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




with st.expander("Mapa"):
  generar_iframe_ubicacion((40.4167047, -3.7035825))
with st.expander("Mapa"):
  generar_iframe_ubicacion((40.4155185, -3.7071406))


with st.expander("Mapa"):
  generar_iframe_ruta((40.4169, -3.7038), (40.4172, -3.7130))
with st.expander("Mapa"):
  generar_iframe_ruta((40.4150, -3.6823), (40.4139, -3.6923))








city = st.text_input(label=":blue[Ciudad a visitar]", placeholder="Escribe tu ciudad...")
recommendations = st.multiselect(':blue[¿Qué quieres visitar?]', ['Restaurantes', 'Monumentos', 'Galerías de arte', 'Museos', 'Pubs', 'Mercadillos', 'Centros comerciales'])
duration = st.number_input(label=":blue[Nº días]", placeholder="Ejemplo: 1 día de visita", step = 1)

if duration == 1:
    horas = st.text_input(label=":blue[¿Qué duración deseas?]", placeholder="Ejemplo: 2 horas de tour turístico")
else:
    horas = None

extra = st.text_input(label=":blue[¿Alguna otra sugerencia para nuestra IA?]", placeholder="Escribe aquí...")

if st.button(label = "Generar el tour turístico", type = "primary"):
     with st.spinner("Generando ... ⏳"):
        st.session_state.responses, st.session_state.planning = get_planning(city, recommendations, duration, horas, extra)

plan, places, routes = st.tabs(['Tour Turístico', 'Información', 'Rutas'])



with plan:
    if 'planning' in st.session_state:
        st.markdown(st.session_state.planning['html_planificacion'], unsafe_allow_html=True)
with places:
  
  if 'responses' in st.session_state:
    st.write ("---")
    
    st.write("## Lugares")
    for i in range(len(st.session_state.planning['orden'])):
        orden = st.session_state.planning['orden'][i]

with routes:
  if 'responses' in st.session_state:
    st.write ("---")

    st.write("## Rutas")
    for i in range(len(st.session_state.planning['orden'])):
        orden = st.session_state.planning['orden'][i]

        for j in range(len(day) - 1):
            st.markdown(f"_**Desde {orden[j]} Hasta {orden[j+1]}**_")
            cord_long_1 = st.session_state.planning['coordenadas_ordenadas'][i][j][0]
            cord_lat_1 = st.session_state.planning['coordenadas_ordenadas'][i][j][1]

            cord_long_2 = st.session_state.planning['coordenadas_ordenadas'][i][j+1][0]
            cord_lat_2 = st.session_state.planning['coordenadas_ordenadas'][i][j+1][1]   
          
            with st.expander("🗺️ Mapa"):
                generar_iframe_ruta(cord_long_1, cord_lat_1, cord_long_2, cord_lat_2)

