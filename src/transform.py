import utils as funciones


def transform_data(raw_data):
    """
    Transforma la respuesta JSON en un DataFrame.
    """

    print("Transformando datos...")

    df = funciones.create_dataFrame(
        raw_data
    )

    print(
        f"Transformación completada. "
        f"Registros: {len(df)}"
    )

    return df