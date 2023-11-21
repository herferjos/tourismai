import openrouteservice

client = openrouteservice.Client(key='5b3ce3597851110001cf6248c946bd142d614eb5ae23bc126f3e9164')

@st.cache_data(persist="disk")
def get_route(coords):
    res = client.directions(coords, profile='foot-walking')
    return res