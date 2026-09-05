import sys   #Directorio raiz
from pathlib import Path
import utils as funciones
import json
from datetime import datetime

# Obtener la ruta del directorio raíz del proyecto (un nivel arriba de /src)
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Ahora tus importaciones funcionarán sin importar desde dónde ejecutes el script
from config.config import API_KEY_WAPI


response = funciones.request_api_weather('Medellín', API_KEY_WAPI)

#Obtener fecha de ejecucion diaria
cutoff_date = datetime.now().strftime("%Y%m%d")
ruta_destino = Path(f"data/raw/clima_medellin_{cutoff_date}.json")


#Guardar el archivo JSON
with open(ruta_destino, "w", encoding="utf-8") as f:
    json.dump(response, f, ensure_ascii=False, indent=4)