import sys   #Directorio raiz
from pathlib import Path
import utils as funciones
import json
from datetime import datetime
import pandas as pd



cutoff_date = datetime.now().strftime("%Y%m%d")
load_json = pd.read_json(f"data/raw/clima_medellin_{cutoff_date}.json")
df = funciones.create_dataFrame(load_json)

df.to_csv(f"data/staged/clima_medellin_{cutoff_date}.csv")



