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


def generar_iframe_ruta(partida, destino, width=1500, height=750):
    # Construir la URL de Google Maps con las coordenadas de partida y destino
    url = f"https://www.google.com/maps/embed?pb=!1m24!1m12!1m3!1d12787.787595039294!2d-4.100142888770666!3d36.74784565619!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m9!3e6!4m3!3m2!1d{partida[0]}!2d{partida[1]}!4m3!3m2!1d{destino[0]}!2d{destino[1]}!5e0!3m2!1ses!2ses"

    # Crear el código del iframe
    iframe_code = f'<div style="text-align: center;"><iframe src="{url}" width="{width}" height="{height}" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'

    st.markdown(iframe_code, unsafe_allow_html=True)

def generar_iframe_ubicacion(ubicacion, width=1500, height=750):
    # Construir la URL de Google Maps con la ubicación dada
    url = f"https://www.google.com/maps/embed?pb=!1m21!1m12!1m3!1d399.59999335038805!2d{ubicacion[1]}!3d{ubicacion[0]}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m6!3e6!4m0!4m3!3m2!1d{ubicacion[0]}!2d{ubicacion[1]}!5e0!3m2!1ses!2ses!4v1704363843022!5m2!1ses!2ses"

    # Crear el código del iframe
    iframe_code = f'<div style="text-align: center;"><iframe src="{url}" width="{width}" height="{height}" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'

    st.markdown(iframe_code, unsafe_allow_html=True)

with st.expander("Mapa"):
  generar_iframe_ubicacion((40.4167047, -3.7035825))
with st.expander("Mapa"):
  generar_iframe_ubicacion((40.4155185, -3.7071406))


with st.expander("Mapa"):
  generar_iframe_ruta((40.4169, -3.7038), (40.4172, -3.7130))
with st.expander("Mapa"):
  generar_iframe_ruta((40.4150, -3.6823), (40.4139, -3.6923))








# city = st.text_input(label=":blue[City to visit]", placeholder="Escribe tu ciudad...")
# recommendations = st.multiselect(':blue[What do you want to visit?]', ['Restaurants', 'Monuments', 'Art Galleries', 'Museums', 'Pubs', 'Street markets', 'Shopping Centers'])
# duration = st.number_input(label=":blue[Nº days]", placeholder="Example: 1 Day Visiting", step = 1)

# if duration == 1:
#     horas = st.text_input(label=":blue[How much time?]", placeholder="Example: 2 hours of Tour")
# else:
#     horas = None

# extra = st.text_input(label=":blue[Any other suggestions]", placeholder="Write here...")

# if st.button(label = "Generate planning tour", type = "primary"):
#      with st.spinner("Generating ... ⏳"):
#         st.session_state.responses, st.session_state.planning = get_planning(city, recommendations, duration, horas, extra)

# plan, places, routes = st.tabs(['Planning', 'Information', 'Routes'])



# # st.write(st.session_state.responses)
# # st.write(st.session_state.planning)


# with plan:
#     if 'planning' in st.session_state:
#         st.markdown(st.session_state.planning['html_planning'], unsafe_allow_html=True)
# with places:

#     st.write ("---")

# with routes:

#     st.write ("---")

#     st.write("## Routes")
#     for i in range(len(st.session_state.planning['order'])):
#         day = st.session_state.planning['order'][i]

#         for j in range(len(day) - 1):
#             st.markdown(f"_**From {day[j]} To {day[j+1]}**_")
#             cord_long_1 = st.session_state.planning['ordered_coordinates'][i][j][0]
#             cord_lat_1 = st.session_state.planning['ordered_coordinates'][i][j][1]

#             cord_long_2 = st.session_state.planning['ordered_coordinates'][i][j+1][0]
#             cord_lat_2 = st.session_state.planning['ordered_coordinates'][i][j+1][1]   

#             m = get_map(day, j, cord_long_1, cord_lat_1, cord_long_2, cord_lat_2)
#             with st.expander("🗺️ Map"):
#                 st_folium(m, width=2000)

