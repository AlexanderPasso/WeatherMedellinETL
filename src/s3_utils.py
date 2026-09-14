import io
import json
import boto3


s3 = boto3.client("s3")


def upload_json(data, bucket, key):
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data, ensure_ascii=False),
        ContentType="application/json"
    )

    print(f"JSON guardado en: s3://{bucket}/{key}")


def upload_dataframe(df, bucket, key):
    buffer = io.StringIO()

    df.to_csv(buffer, index=False)

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=buffer.getvalue(),
        ContentType="text/csv"
    )

    print(f"CSV guardado en: s3://{bucket}/{key}")