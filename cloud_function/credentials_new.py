import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), 'configs', '.env'))
#load_dotenv('.env')


########################## GOOGLE CLOUD CREDENTIALS ##########################
BUCKET_NAME = os.getenv('bucket_name')
GCLOUD_PROJECT = os.getenv('gcp_project_id')
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(os.getcwd(), 'configs', 'service_account_key.json')