import openrouteservice
import streamlit as st
from openai import OpenAI
from langchain.tools import DuckDuckGoSearchRun
import json
import folium

client = OpenAI(api_key = st.secrets['openai_key'])

client2 = openrouteservice.Client(key=st.secrets['route_key'])

search = DuckDuckGoSearchRun()

@st.cache_data(persist="disk")
def get_map(cord_long_1, cord_lat_1, cord_long_2, cord_lat_2):

    m = folium.Map(location=[cord_lat_1,cord_long_1], zoom_start = 16)

    folium.Marker(
        location=[cord_long_1, cord_lat_1],
        popup=day[j],
        icon=folium.Icon(color="red"),
    ).add_to(m)

    folium.Marker(
        location=[cord_long_2, cord_lat_2],
        popup=day[j+1],
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
        else:
            busqueda = ""
        # extractor_prompt = [{"role":"system", "content": "Eres mi asistente, y me tienes que ayudar a extraer los lugares más importantes que visistar para la petición del usuario. Responde siempre en JSON con la siguiente estructura: {'lugares': [<nombre de los lugares a visitar>], 'informacion': [<informacion relevante del lugar>]}"}]
        # extractor_prompt.append({"role":"user", "content": f"""El usuario desea encontrar lo siguiente: {query}
        #                         Esto ha sido lo que he encontrado en internet: {busqueda}
        #                         Recuerda responder en JSON únicamente con lo que te he pedido"""})
        extractor_prompt = [{"role":"system", "content": "You are my assistant, and you need to help me extract the most important places to visit for the user's request. Always respond in JSON with the following structure: {'places': [<name of the places to visit>], 'information': [<relevant information about the place>]}"}]
        extractor_prompt.append({"role":"user", "content": f"""The user wants to find the following: {query}
                                        
                                        Remember to respond in JSON format only with what I have asked for"""})

        respuesta = chat(extractor_prompt)

        # se podria buscar tambien informacion sobre lugares, y no depende de una unica busqueda

        respuesta['coordenadas'] = []

        for lugar in respuesta['places']:
            query = f"coordinates (longitude/latitude) of {lugar} in {city} "
            busqueda = search.run(query)
            # coordenadas_prompt = [{"role":"system", "content": "Eres mi asistente, y me tienes que ayudar a extraer los lugares más importantes que visistar para la petición del usuario. Responde siempre en JSON con la siguiente estructura: {'lugares': [<nombre de los lugares a visitar>], 'coordenadas': [<coordenadas de cada lugar en longitud/latitud>]}"}]
            # coordenadas_prompt.append({"role":"user", "content": f"""El usuario desea encontrar las {query}
            #                         Esto ha sido lo que he encontrado en internet: {busqueda}
            #                         Recuerda responder en JSON únicamente con lo que te he pedido"""})
            coordenadas_prompt = [{"role":"system", "content": "You are my assistant, and you need to help me extract the most important places to visit for the user's request. Always respond in JSON with the following structure: {'places': [<name of the places to visit>], 'coordinates': [<coordinates of each place in longitude/latitude>]}"}]
            coordenadas_prompt.append({"role":"user", "content": f"""The user wants to find {query}
                                                This is what I found on the internet: {busqueda}
                                                Remember to respond in JSON format only with what I have asked for. Coordinate format: (longitude/latitude)"""})

            coordenadas = chat(coordenadas_prompt)
            respuesta['coordenadas'].append(coordenadas)

        print(respuesta)
        responses.append(respuesta)

    if horas == "":
        pass
    else:
        horas = f"El usuario específica que debe durar: {horas}"

    if extra == "":
        pass
    else:
        extra = f"Información extra del usuario: {extra}"

    # planning_prompt = [{"role":"system", "content": "Eres mi asistente de turismo, y me tienes que ayudar a hacer un planning para mis turistas. Te voy a dar toda la información necesaria para construir el planning de turismo: ciudad, lugares, duracion e instrucciones extra del usuario. Te función será devolverme un string en formato HTML para enseñarlo en la web, así haz uso de todas las herramientas de html para destacar y poner bonito el texto. También deberás proporcionarme el orden de visita de los lugares, es decir, puedes visitar todos los lugares en 1 día si el usuario te pide un planning para un día, o puedes visitar en varios días, entonces en el orden deberás escribir una lista de los lugares ordenados por orden de visita en listas de días. Ejemplo: [['lugar_1', 'lugar_2'], ['lugar_3', lugar_4']]. Aquí se ha visitado el lugar_1 y lugar_2 en el 1º día y el lugar_3 y lugar_4 en el 2º día. Recuerda también proporcionar las coordenadas en el mismo orden y mantener el formato de las coordenadas en: (longitud,latitud). Tu ouput deberá ser un JSON así: {'html_planning': <aquí el string del html que voy a printar>, 'orden': [<lista lugares ordenadas por orden de visita y de día en listas de listas>], 'coordenadas_ordenadas':[<lista de coordenadas de lugares a visitar en orden, y por días en listas de listas>]}"}]
    # planning_prompt.append({"role":"user", "content": f"""Estas son los detalles para elaborar el planning de turismo:
    #                         Ciudad: {city}
    #                         Lugares: {responses}
    #                         Duración del tour: {duration} día(s). {horas}
    #                         {extra}
    #                         Recuerda responder en JSON únicamente con lo que te he pedido"""})
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