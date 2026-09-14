import pandas as pd
import requests
from tqdm import tqdm


def request_api_weather(query, api_key):
    """
    Obtiene los datos meteorológicos desde Weather API.

    Parameters
    ----------
    query : str
        Ciudad a consultar.
    api_key : str
        API Key de Weather API.

    Returns
    -------
    dict
        Respuesta JSON de la API.
    """

    url_clima = (
        "http://api.weatherapi.com/v1/forecast.json"
        f"?key={api_key}"
        f"&q={query}"
        "&days=1"
        "&aqi=no"
        "&alerts=no"
    )

    try:
        response = requests.get(url_clima, timeout=30) #Para que lambda no espere mas de 30 segundos si hay problema con la AP
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error consultando Weather API: {e}")
        raise


def get_forecast(response, i):
    """
    Extrae la información de una hora específica
    del pronóstico.
    """

    fecha = (
        response["forecast"]["forecastday"][0]["hour"][i]["time"]
        .split()[0]
    )

    hora = int(
        response["forecast"]["forecastday"][0]["hour"][i]["time"]
        .split()[1]
        .split(":")[0]
    )

    condicion = (
        response["forecast"]["forecastday"][0]["hour"][i]
        ["condition"]["text"]
    )

    temperatura = (
        response["forecast"]["forecastday"][0]["hour"][i]["temp_c"]
    )

    rain = (
        response["forecast"]["forecastday"][0]["hour"][i]
        ["will_it_rain"]
    )

    prob_rain = (
        response["forecast"]["forecastday"][0]["hour"][i]
        ["chance_of_rain"]
    )

    return (
        fecha,
        hora,
        condicion,
        temperatura,
        rain,
        prob_rain
    )


def create_dataFrame(response):
    """
    Convierte la respuesta JSON de Weather API
    en un DataFrame.
    """

    columns = [
        "Fecha",
        "Hora",
        "Condicion_Clima",
        "Temperatura",
        "Lluvia",
        "Probabilidad_Lluvia"
    ]

    num_registros = len(
        response["forecast"]["forecastday"][0]["hour"]
    )

    datos = []

    for i in tqdm(
        range(num_registros),
        colour="green"
    ):
        datos.append(
            get_forecast(response, i)
        )

    df = pd.DataFrame(
        datos,
        columns=columns
    )

    return df