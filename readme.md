## 📁 Estructura del Repositorio

```text

├── app/
|   └── main.py
|
├── data/
|   ├── master/
|   |   └── clima_medellin.csv
|   ├── raw
|   |   └── clima_medellin_{fecha}.csv
|   └── staged
|       └── clima_medellin_{fecha}.csv
|
├── src/
│   ├── extract.py         # Módulo de extracción de API
│   ├── transform.py       # Módulo de limpieza y conversión datetime
│   ├── load.py            # 
|   └── utils.py
|    
├── .gitignore                   
├── requirements.txt       # Dependencias del proyecto
└── README.md
```


## Ejecutar streamlit
    - streamlit run app/main.py

## Guardar archivo requirmentes
    - pipreqs . --force

