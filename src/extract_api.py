from datetime import datetime
from zoneinfo import ZoneInfo


import utils as funciones


def extract_data(api_key):
    """
    Extrae los datos de clima desde Weather API.
    """

    print("Consultando Weather API...")

    response = funciones.request_api_weather(
        "Medellín",
        api_key
    )

    cutoff_date = datetime.now(
        ZoneInfo("America/Bogota")
    ).strftime("%Y%m%d")

    print(
        f"Extracción completada. "
        f"Fecha de ejecución: {cutoff_date}"
    )

    return response, cutoff_date