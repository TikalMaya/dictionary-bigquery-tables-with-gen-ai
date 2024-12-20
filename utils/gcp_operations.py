from google.cloud import storage
from credentials import BUCKET_NAME
import json


class CloudStorageHandler:
    def __init__(self):
        """
        Initializes the CloudStorageHandler with the specified bucket name.
        """

        self.bucket_name = BUCKET_NAME
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def save_to_bucket(self, dataset_name, table_name, description):
        """
        Saves the AI-generated description to a Google Cloud Storage bucket as a JSON file.
        """
        # Define the file path and content
        file_path = f"{dataset_name}/{table_name}_description.json"
        blob = self.bucket.blob(file_path)

        # Convert description to JSON and upload
        description_json = json.dumps(description, ensure_ascii=False, indent=4)
        blob.upload_from_string(description_json, content_type="application/json")

        print(f"Saved description for table {table_name} to {file_path} in bucket {self.bucket_name}")
