import json
import streamlit as st
from modules import get_planning, get_map

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



import streamlit as st
import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app
components.iframe("https://www.google.es/maps/dir/40.4167047,-3.7035825/40.4179,-3.7144/")





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

