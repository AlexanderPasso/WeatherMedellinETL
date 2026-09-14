import io

import boto3
import pandas as pd


s3 = boto3.client("s3")


def load_master(bucket):
    """
    Lee todos los archivos staged de S3,
    los concatena y genera el archivo master.
    """

    prefix = "staged/"

    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    archivos = []

    for obj in response.get("Contents", []):

        key = obj["Key"]

        if key.endswith(".csv"):
            archivos.append(key)

    if not archivos:
        raise Exception(
            "No existen archivos staged en S3."
        )

    lista_df = []

    for key in sorted(archivos):

        print(
            f"Leyendo: s3://{bucket}/{key}"
        )

        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        df = pd.read_csv(
            io.BytesIO(
                response["Body"].read()
            )
        )

        lista_df.append(df)

    df_master = pd.concat(
        lista_df,
        ignore_index=True
    )

    # Eliminar columna innecesaria
    if "Unnamed: 0" in df_master.columns:
        df_master = df_master.drop(
            columns=["Unnamed: 0"]
        )

    # Guardar master
    buffer = io.StringIO()

    df_master.to_csv(
        buffer,
        index=False
    )

    master_key = "master/clima_medellin.csv"

    s3.put_object(
        Bucket=bucket,
        Key=master_key,
        Body=buffer.getvalue(),
        ContentType="text/csv"
    )

    print(
        f"Master generado: "
        f"s3://{bucket}/{master_key}"
    )

    return df_master