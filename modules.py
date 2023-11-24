import openrouteservice
import streamlit as st
from openai import OpenAI
from langchain.tools import DuckDuckGoSearchRun
import json
import folium
from openrouteservice import convert

client = OpenAI(api_key = st.secrets['openai_key'])

client2 = openrouteservice.Client(key=st.secrets['route_key'])

search = DuckDuckGoSearchRun()

@st.cache_data(persist="disk")
def get_map(day,j, cord_long_1, cord_lat_1, cord_long_2, cord_lat_2):

    m = folium.Map(location=[cord_lat_1,cord_long_1], zoom_start = 20)

    folium.Marker(
        location=[cord_long_1, cord_lat_1],
        popup=f"{day[j]}",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    folium.Marker(
        location=[cord_long_2, cord_lat_2],
        popup=f"{day[j+1]}",
        icon=folium.Icon(color="red"),
    ).add_to(m) 

    route = get_route(((cord_long_1, cord_lat_1), (cord_long_2, cord_lat_2)))
    geometry = route['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)
    distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(route['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
    duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(route['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=800)).add_to(m)

    return m

@st.cache_data(persist="disk")
def get_route(coords):
    res = client2.directions(coords, profile="foot-walking")
    return res


def get_planning(city, recommendations, duration, horas, extra):
    responses = []
    for recommendation in recommendations:
        query = f"{recommendation} en {city}"
        if recommendation != "Monuments" or "Museums" or "Art Galleries":
            busqueda = search.run(query)
            busqueda = f"This is what I found on the internet: {busqueda}"

            extractor_prompt = [{"role":"system", "content": "You are my assistant, and you need to help me extract the most important places to visit for the user's request. Always respond in JSON with the following structure: {'places': [<name of the places to visit>]}"}]
            extractor_prompt.append({"role":"user", "content": f"""The user wants to find the following: {query}
                                            {busqueda}
                                            Remember to respond in JSON format only with what I have asked for"""})

            lugares = chat(extractor_prompt)['places']
            busquedas = []
            for lugar in lugares:
                busqueda = search.run(lugar)
                busquedas.append(busqueda)

            extractor_prompt = [{"role":"system", "content": "You are my assistant, and you need to help me extract the most important information of the places for the user's request. Always respond in JSON with the following structure: {'places': [<name of the places to visit>], 'information': [<relevant information about the place>]}"}]
            extractor_prompt.append({"role":"user", "content": f"""The user wants to visit {lugares} in {city}. Please give all information you know about that places.
                                            Information I found on internet: {busquedas}
                                            Remember to respond in JSON format only with what I have asked for"""})
                    
            respuesta = chat(extractor_prompt)
            responses.append(respuesta)
        else:
            extractor_prompt = [{"role":"system", "content": "You are my assistant, and you need to help me generate the most important places to visit for the user's request. Always respond in JSON with the following structure: {'places': [<name of the places to visit>], 'information': [<relevant information about the place>]}"}]
            extractor_prompt.append({"role":"user", "content": f"""The user wants to visit {city} for {recommendation}. Please give all information you know about places
                                            Remember to respond in JSON format only with what I have asked for"""})

            respuesta = chat(extractor_prompt)
            responses.append(respuesta)
            
        respuesta['coordenadas'] = []

        for lugar in respuesta['places']:
            query = f"coordinates (longitude/latitude) of {lugar} in {city} "
            busqueda = search.run(query)
            coordenadas_prompt = [{"role":"system", "content": "You are my assistant, and you need to help me extract the most important places to visit for the user's request. Always respond in JSON with the following structure: {'places': [<name of the places to visit>], 'coordinates': [<coordinates of each place in longitude/latitude>]}"}]
            coordenadas_prompt.append({"role":"user", "content": f"""The user wants to find {query}
                                                This is what I found on the internet: {busqueda}
                                                Remember to respond in JSON format only with what I have asked for. Coordinate format: (longitude/latitude)"""})

            coordenadas = chat(coordenadas_prompt)
            respuesta['coordenadas'].append(coordenadas)

        responses.append(respuesta)

    if horas == "":
        pass
    else:
        horas = f"El usuario específica que debe durar: {horas}"

    if extra == "":
        pass
    else:
        extra = f"Información extra del usuario: {extra}"

    planning_prompt = [{"role":"system", "content": "You are my tourism assistant, and you need to help me create an itinerary for my tourists. I will provide you with all the necessary information to build the tourism itinerary: city, places, duration, and any additional user instructions. Your function is to return an HTML-formatted string to display on the web, so make use of all HTML tools to highlight and beautify the text. You also need to provide me with the order of visiting places, meaning you can visit all places in 1 day if the user requests a one-day itinerary, or you can spread it over multiple days. In the order, you should write a list of places ordered by the visit order in lists of days. Example: [['place_1', 'place_2'], ['place_3', 'place_4']]. Here, place_1 and place_2 are visited on the 1st day, and place_3 and place_4 on the 2nd day. Also, remember to provide the coordinates in the same order and maintain the format of coordinates as: (longitude, latitude). Your output should be in JSON format as follows: {'html_planning': <here goes the HTML string to be printed>, 'order': [<list of places ordered by visit order and day in lists of lists>], 'ordered_coordinates':[<list of coordinates of places to visit in order, and by days in lists of lists>]}"}]
    planning_prompt.append({"role":"user", "content": f"""Here are the details to create the tourism itinerary:
                                City: {city}
                                Places: {responses}
                                Tour Duration: {duration} day(s). {horas}
                                {extra}
                                Remember to respond in JSON format only with what I have asked for"""})

    planning = chat(planning_prompt)

    return responses, planning

def chat(messages):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=messages,
    response_format={"type": "json_object"},
  )

  return json.loads(response.choices[0].message.content)