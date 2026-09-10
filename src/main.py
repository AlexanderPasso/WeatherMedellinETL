import extract_api
import transform
import load

def run_pipeline():
    print("---- Extrayendo datos de la API -----")
    extract_api

    print("---- Transformando datos ----")
    transform

    print("---- Cargando datos a S3 ----- ")
    load

    print("Pipeline ETL completado con éxito")

# Función de entrada requerida por AWS Lambda
def lambda_handler(event, context):
    try:
        run_pipeline()
        return {
            'statusCode': 200,
            'body': 'ETL ejecutada correctamente'
        }
    except Exception as e:
        print(f"Error durante la ejecución del pipeline: {str(e)}")
        raise e

# Permite probarlo localmente antes de subir a AWS
if __name__ == "__main__":
    run_pipeline()