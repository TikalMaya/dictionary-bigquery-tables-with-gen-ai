from google.cloud import bigquery
import pandas as pd


class BigQueryHandler:
    def __init__(self):
        """
        Initializes the BigQueryHandler and the BigQuery client.
        """
        self.client = bigquery.Client()

    def fetch_table_rows(self, dataset_name, table_name, first_n=5, last_n=5):
        """
        Fetches the first `first_n` rows and last `last_n` rows from a BigQuery table.
        """
        # Fetch first N rows
        first_rows_query = f"SELECT * FROM `{dataset_name}.{table_name}` ORDER BY 1 ASC LIMIT {first_n}"
        first_rows = self.client.query(first_rows_query).to_dataframe()
        #first_rows=pd.read_gbq(first_rows_query)
        # Fetch last N rows
        last_rows_query = f"SELECT * FROM `{dataset_name}.{table_name}` ORDER BY 1 DESC LIMIT {last_n}"
        last_rows = self.client.query(last_rows_query).to_dataframe()

        # Concatenate the two DataFrames
        return pd.concat([first_rows, last_rows])

    def list_tables_in_dataset(self, dataset_name):
        """
        Lists all tables in a given BigQuery dataset.
        """
        dataset_ref = self.client.dataset(dataset_name)
        tables = list(self.client.list_tables(dataset_ref))
        return [table.table_id for table in tables]
