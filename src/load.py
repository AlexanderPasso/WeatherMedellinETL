import sys   #Directorio raiz
from pathlib import Path
import utils as funciones
import pandas as pd 
import glob



archivos = sorted(glob.glob("data/staged/clima_medellin_*.csv"))

# Crear una lista de dataframes y unirlos
lista_df = [pd.read_csv(archivo) for archivo in archivos]
df= pd.concat(lista_df, ignore_index=True)
if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        
print(df)

df.to_csv(f"data/master/clima_medellin.csv")

