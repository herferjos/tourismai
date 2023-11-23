import openrouteservice
import streamlit as st

client = openrouteservice.Client(key='5b3ce3597851110001cf6248c946bd142d614eb5ae23bc126f3e9164')

@st.cache_data(persist="disk")
def get_route(coords):
    res = client.directions(coords, profile="foot-walking")
    return res


def get_planning(city, recommendations, duration, horas, extra):
    responses = []
    for recommnedation in recommendations:
        query = f"{recommnedation} en {city}"
        busqueda = search.run(query)
        extractor_prompt = [{"role":"system", "content": "Eres mi asistente, y me tienes que ayudar a extraer los lugares más importantes que visistar para la petición del usuario. Responde siempre en JSON con la siguiente estructura: {'lugares': [<nombre de los lugares a visitar>], 'informacion': [<informacion relevante del lugar>]}"}]
        extractor_prompt.append({"role":"user", "content": f"""El usuario desea encontrar lo siguiente: {query}
                                Esto ha sido lo que he encontrado en internet: {busqueda}
                                Recuerda responder en JSON únicamente con lo que te he pedido"""})
        respuesta = chat(extractor_prompt)

        # se podria buscar tambien informacion sobre lugares, y no depende de una unica busqueda

        respuesta['coordenadas'] = []

        for lugar in respuesta['lugares']:
            query = f"coordenadas de {lugar} en {ciudad}"
            busqueda = search.run(query)
            coordenadas_prompt = [{"role":"system", "content": "Eres mi asistente, y me tienes que ayudar a extraer los lugares más importantes que visistar para la petición del usuario. Responde siempre en JSON con la siguiente estructura: {'lugares': [<nombre de los lugares a visitar>], 'coordenadas': [<coordenadas de cada lugar en longitud/latitud>]}"}]
            coordenadas_prompt.append({"role":"user", "content": f"""El usuario desea encontrar las {query}
                                    Esto ha sido lo que he encontrado en internet: {busqueda}
                                    Recuerda responder en JSON únicamente con lo que te he pedido"""})
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

    planning_prompt = [{"role":"system", "content": "Eres mi asistente de turismo, y me tienes que ayudar a hacer un planning para mis turistas. Te voy a dar toda la información necesaria para construir el planning de turismo: ciudad, lugares, duracion e instrucciones extra del usuario. Te función será devolverme un string en formato HTML para enseñarlo en la web, así haz uso de todas las herramientas de html para destacar y poner bonito el texto. También deberás proporcionarme el orden de visita de los lugares, es decir, puedes visitar todos los lugares en 1 día si el usuario te pide un planning para un día, o puedes visitar en varios días, entonces en el orden deberás escribir una lista de los lugares ordenados por orden de visita en listas de días. Ejemplo: [['lugar_1', 'lugar_2'], ['lugar_3', lugar_4']]. Aquí se ha visitado el lugar_1 y lugar_2 en el 1º día y el lugar_3 y lugar_4 en el 2º día. Tu ouput deberá ser un JSON así: {'html_planning': <aquí el string del html que voy a printar>, 'orden': [<lista lugares ordenadas por orden de visita>]}"}]
    planning_prompt.append({"role":"user", "content": f"""Estas son los detalles para elaborar el planning de turismo:
                            Ciudad: {city}
                            Lugares: {responses}
                            Duración del tour: {duration} día(s). {horas}
                            {extra}
                            Recuerda responder en JSON únicamente con lo que te he pedido"""})
    planning = chat(planning_prompt)

    return responses, planning
