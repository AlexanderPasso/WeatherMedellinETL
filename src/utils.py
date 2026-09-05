import os
from twilio.rest import Client
import time 
import sys   #Directorio raiz
from pathlib import Path
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from tqdm import tqdm

from datetime import datetime

# Obtener la ruta del directorio raíz del proyecto (un nivel arriba de /src)
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Ahora tus importaciones funcionarán sin importar desde dónde ejecutes el script
from config.config import API_KEY_WAPI



def request_api_weather(query,api_key):
    #query: Ciudad
    #api_key: Codigo generado por la cuenta creada en https://www.weatherapi.com/

    url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try:
        response = requests.get(url_clima).json()
    except Exception as e:
        print(e)

    return response

#Funcion para obtener los datos desde el json
def get_forecast(response,i):
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    temperatura = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return fecha,hora, condicion,temperatura,rain,prob_rain

def create_dataFrame(response):
    #Creacion dataframe
    col = ['Fecha','Hora','Condicion_Clima','Temperatura','Lluvia','Probabilidad_Lluvia']
    num_registros = len(response['forecast']['forecastday'][0]['hour'])
    datos = []

    #tqdm es una libreria que permite observar una barra de progreso o carga
    for i in tqdm(range(num_registros), colour='green'):
        datos.append(get_forecast(response,i))

    df = pd.DataFrame(datos, columns=col)
    return df