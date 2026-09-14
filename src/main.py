import os

from extract_api import extract_data
from transform import transform_data
from load import load_master
from s3_utils import upload_json, upload_dataframe

#S3_BUCKET: etl-clima-medellin-data

BUCKET = os.environ["S3_BUCKET"]
API_KEY = os.environ["API_KEY_WAPI"]


def run_pipeline():

    print("==============================")
    print("INICIANDO PIPELINE ETL")
    print("==============================")

    # =====================================
    # 1. EXTRACT
    # =====================================

    print("\n---- EXTRACT ----")

    raw_data, cutoff_date = extract_data(
        API_KEY
    )

    raw_key = (
        f"raw/"
        f"clima_medellin_{cutoff_date}.json"
    )

    
    upload_json(
        raw_data,
        BUCKET,
        raw_key
    )

    # =====================================
    # 2. TRANSFORM
    # =====================================

    print("\n---- TRANSFORM ----")

    df = transform_data(
        raw_data
    )

    staged_key = (
        f"staged/"
        f"clima_medellin_{cutoff_date}.csv"
    )

    upload_dataframe(
        df,
        BUCKET,
        staged_key
    )

    # =====================================
    # 3. LOAD
    # =====================================

    print("\n---- LOAD ----")

    df_master = load_master(
        BUCKET
    )

    print(
        f"Master actualizado. "
        f"Registros totales: {len(df_master)}"
    )

    print("\n==============================")
    print("PIPELINE ETL COMPLETADO")
    print("==============================")


def lambda_handler(event, context):

    try:

        run_pipeline()

        return {
            "statusCode": 200,
            "body": "ETL ejecutado correctamente"
        }

    except Exception as e:

        print(
            f"Error durante el pipeline: {e}"
        )

        raise


if __name__ == "__main__":

    run_pipeline()