import os
from google.cloud import storage
from credentials_new import BUCKET_NAME,GCLOUD_PROJECT,GOOGLE_APPLICATION_CREDENTIALS
import json

os.environ["GCLOUD_PROJECT"] = GCLOUD_PROJECT
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

class CloudStorageHandler:
    def __init__(self):
        """
        Initializes the CloudStorageHandler with the specified bucket name.
        """

        self.bucket_name1 = BUCKET_NAME
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name1)

    def save_to_bucket(self, dataset_name, table_name, description):
        """
        Saves the AI-generated description to a Google Cloud Storage bucket as a JSON file.
        """
        from json import dumps

        # Initialize the Storage client
        storage_client = storage.Client()
        self.bucket_name1=BUCKET_NAME
        bucket = storage_client.bucket(self.bucket_name1)
        print("-------------BUCKET NAME-------",self.bucket_name1)
        # Define the file path and content
        file_path = f"{dataset_name}/{table_name}_description.json"
        blob = bucket.blob(file_path)

        # Convert description to JSON and upload
        description_json = dumps(description, ensure_ascii=False, indent=4)
        blob.upload_from_string(description_json, content_type="application/json")

        print(f"Saved description for table {table_name} to {file_path} in bucket {self.bucket_name1}")
