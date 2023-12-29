import streamlit as st
from openai import OpenAI
from langchain.tools import DuckDuckGoSearchRun
import json

client = OpenAI(api_key = st.secrets['openai_key'])

search = DuckDuckGoSearchRun()

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
