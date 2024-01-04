import streamlit as st
from openai import OpenAI
from langchain.tools import DuckDuckGoSearchRun
import json

client = OpenAI(api_key = st.secrets['openai_key'])

search = DuckDuckGoSearchRun()

def get_planning(ciudad, recomendaciones, duracion, horas, extra):
    respuestas = []
    for recomendacion in recomendaciones:
        consulta = f"{recomendacion} en {ciudad}"
        if recomendacion != "Monumentos" or "Museos" or "Galerías de arte":
            busqueda = search.run(consulta)
            busqueda = f"Esto es lo que encontré en internet: {busqueda}"

            extractor_prompt = [{"role":"system", "content": "Eres mi asistente y necesitas ayudarme a extraer los lugares más importantes para visitar según la solicitud del usuario. Siempre responde en JSON con la siguiente estructura: {'lugares': [<nombre de los lugares para visitar>]}"}]
            extractor_prompt.append({"role":"user", "content": f"""El usuario desea encontrar lo siguiente: {consulta}
                                            {busqueda}
                                            Recuerda responder solo en formato JSON con lo que he solicitado."""})

            lugares = chat(extractor_prompt)['lugares']
            busquedas = []
            for lugar in lugares:
                busqueda = search.run(lugar)
                busquedas.append(busqueda)

            extractor_prompt = [{"role":"system", "content": "Eres mi asistente y necesitas ayudarme a extraer la información más importante de los lugares según la solicitud del usuario. Siempre responde en JSON con la siguiente estructura: {'lugares': [<nombre de los lugares para visitar>], 'informacion': [<información relevante sobre el lugar>]}"}]
            extractor_prompt.append({"role":"user", "content": f"""El usuario desea visitar {lugares} en {ciudad}. Por favor, proporciona toda la información que sepas sobre esos lugares.
                                            Información que encontré en internet: {busquedas}
                                            Recuerda responder solo en formato JSON con lo que he solicitado."""})
                    
            respuesta = chat(extractor_prompt)
            respuestas.append(respuesta)
        else:
            extractor_prompt = [{"role":"system", "content": "Eres mi asistente y necesitas ayudarme a generar los lugares más importantes para visitar según la solicitud del usuario. Siempre responde en JSON con la siguiente estructura: {'lugares': [<nombre de los lugares para visitar>], 'informacion': [<información relevante sobre el lugar>]}"}]
            extractor_prompt.append({"role":"user", "content": f"""El usuario desea visitar {ciudad} por {recomendacion}. Por favor, proporciona toda la información que sepas sobre los lugares.
                                            Recuerda responder solo en formato JSON con lo que he solicitado."""})

            respuesta = chat(extractor_prompt)
            respuestas.append(respuesta)
            
        respuesta['coordenadas'] = []

        for lugar in respuesta['lugares']:
            consulta = f"coordenadas (longitud/latitud) de {lugar} en {ciudad} "
            busqueda = search.run(consulta)
            coordenadas_prompt = [{"role":"system", "content": "Eres mi asistente y necesitas ayudarme a extraer los lugares más importantes para visitar según la solicitud del usuario. Siempre responde en JSON con la siguiente estructura: {'lugares': [<nombre de los lugares para visitar>], 'coordenadas': [<coordenadas de cada lugar en longitud/latitud>]}"}]
            coordenadas_prompt.append({"role":"user", "content": f"""El usuario desea encontrar {consulta}
                                                Esto es lo que encontré en internet: {busqueda}
                                                Recuerda responder solo en formato JSON con lo que he solicitado. Formato de coordenadas: (longitud/latitud)"""})

            coordenadas = chat(coordenadas_prompt)
            respuesta['coordenadas'].append(coordenadas)

        respuestas.append(respuesta)

    if horas == "":
        pass
    else:
        horas = f"El usuario especifica que debe durar: {horas}"

    if extra == "":
        pass
    else:
        extra = f"Información extra del usuario: {extra}"

    planning_prompt = [{"role":"system", "content": "Eres mi asistente turístico y necesitas ayudarme a crear un itinerario para mis turistas. Te proporcionaré toda la información necesaria para construir el itinerario turístico: ciudad, lugares, duración e instrucciones adicionales del usuario. Tu función es devolver una cadena con formato HTML para mostrar en la web, así que utiliza todas las herramientas de HTML para resaltar y embellecer el texto. También debes proporcionarme el orden de visita de los lugares, lo que significa que puedes visitar todos los lugares en 1 día si el usuario solicita un itinerario de un día, o puedes distribuirlo en varios días. En el orden, debes escribir una lista de lugares ordenados por el orden de visita en listas de días. Ejemplo: [['lugar_1', 'lugar_2'], ['lugar_3', 'lugar_4']]. Aquí, lugar_1 y lugar_2 se visitan el primer día, y lugar_3 y lugar_4 el segundo día. Además, recuerda proporcionar las coordenadas en el mismo orden y mantener el formato de coordenadas como: (longitud, latitud). Tu salida debe estar en formato JSON de la siguiente manera: {'html_planificacion': <aquí va la cadena HTML para imprimir>, 'orden': [<lista de lugares ordenados por orden de visita y día en listas de listas>], 'coordenadas_ordenadas':[<lista de coordenadas de lugares para visitar en orden y por días en listas de listas>]}"}]
    planning_prompt.append({"role":"user", "content": f"""Aquí están los detalles para crear el itinerario turístico:
                                Ciudad: {ciudad}
                                Lugares: {respuestas}
                                Duración del tour: {duracion} día(s). {horas}
                                {extra}
                                Recuerda responder solo en formato JSON con lo que he solicitado."""})

    planificacion = chat(planning_prompt)

    return respuestas, planificacion

def chat(messages):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=messages,
    response_format={"type": "json_object"},
  )

  return json.loads(response.choices[0].message.content)


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
