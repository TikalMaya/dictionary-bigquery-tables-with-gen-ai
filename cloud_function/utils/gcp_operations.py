
import json
from google.cloud import storage, bigquery, secretmanager
from utils.credentials import BUCKET_NAME, GCLOUD_PROJECT
from google.cloud.bigquery import SchemaField
import google_crc32c
# import pandas_gbq as pd
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from pandas import DataFrame

credentials = service_account.Credentials.from_service_account_file('configs/service_account_key.json')
# Initialize BigQuery client
client = bigquery.Client(credentials= credentials,project=GCLOUD_PROJECT)

from google.cloud import bigquery, storage
import pandas as pd

def get_first_and_last_rows(bq_client, dataset_name, table_name):
    """
    Fetches the first 5 rows and last 5 rows of the specified BigQuery table.
    """
    # Fetch first 5 rows
    first_rows_query = f"SELECT * FROM `{dataset_name}.{table_name}` ORDER BY 1 ASC LIMIT 5"
    first_rows = bq_client.query(first_rows_query).to_dataframe()

    # Fetch last 5 rows
    last_rows_query = f"SELECT * FROM `{dataset_name}.{table_name}` ORDER BY 1 DESC LIMIT 5"
    last_rows = bq_client.query(last_rows_query).to_dataframe()

    # Concatenate the two DataFrames
    return pd.concat([first_rows, last_rows])

def save_to_cloud_storage(bucket_name, dataset_name, table_name, description):
    """
    Saves the AI-generated description to a Google Cloud Storage bucket as a JSON file.
    """
    from json import dumps

    # Initialize the Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Define the file path and content
    file_path = f"{dataset_name}/{table_name}_description.json"
    blob = bucket.blob(file_path)

    # Convert description to JSON and upload
    description_json = dumps(description, ensure_ascii=False, indent=4)
    blob.upload_from_string(description_json, content_type="application/json")

    print(f"Saved description for table {table_name} to {file_path} in bucket {bucket_name}")


