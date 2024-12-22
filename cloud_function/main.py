from bigquery_fun import BigQueryHandler
import sys
import os

# Add the parent directory (root of the repo) to the system path
#file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from gcp_operations_fun import CloudStorageHandler
from ai_agent_fun import generate_chatgpt_description
from ai_agent_fun import generate_gemini_description


def generate_ai_descriptions(table_sample, ai_model):
    """
    Generates AI-based descriptions in Spanish for the given table sample using the specified model.
    """
    if ai_model == "chatgpt":
        return generate_chatgpt_description(table_sample)
    elif ai_model == "gemini":
        return generate_gemini_description(table_sample)
    else:
        raise ValueError(f"Unsupported AI model: {ai_model}")


def process_dataset(request):
    """
    Main entry point for processing datasets and generating descriptions.
    """
    # Fetch query parameters
    dataset_name = request.args.get("dataset_name")
    table_name = request.args.get("table_name")
    ai_model = request.args.get("ai_model")

    # Validate input parameters
    if not dataset_name:
        return {"error": "dataset_name is required"}, 400

    # Initialize handlers
    bigquery_handler = BigQueryHandler()
    cloud_storage_handler = CloudStorageHandler()
    if not ai_model:
        print("Testing ChatGPT helper...")
        try:
            table_sample = bigquery_handler.fetch_table_rows(dataset_name, table_name)
            chatgpt_result = generate_chatgpt_description(table_sample)
            print("ChatGPT Description:\n", chatgpt_result)
        except Exception as e:
            print("ChatGPT Test Failed:", e)

        print("\nTesting Gemini helper...")
        try:
            table_sample = bigquery_handler.fetch_table_rows(dataset_name, table_name)
            gemini_result = generate_gemini_description(table_sample)
            print("Gemini Description:\n", gemini_result)
        except Exception as e:
            print("Gemini Test Failed:", e)
        return {"status": "successfully generated both discriptions"}, 200

    # If table_name is provided, process a single table
    if table_name:
        table_sample = bigquery_handler.fetch_table_rows(dataset_name, table_name)
        ai_response = generate_ai_descriptions(table_sample, ai_model)
        cloud_storage_handler.save_to_bucket(dataset_name, table_name, ai_response)
        return {"status": "success", "description": ai_response}, 200

    # If table_name is not provided, process all tables in the dataset
    table_list = bigquery_handler.list_tables_in_dataset(dataset_name)
    results = []
    for table_name in table_list:
        table_sample = bigquery_handler.fetch_table_rows(dataset_name, table_name)
        ai_response = generate_ai_descriptions(table_sample, ai_model)
        print("Done")
        cloud_storage_handler.save_to_bucket(dataset_name, table_name, ai_response)
        results.append({
            "table_name": table_name,
            "description": ai_response
        })

    return {"status": "success", "results": results}, 200


def process_dataset_main():
    """
    Main entry point for processing datasets and generating descriptions.
    """
    # Fetch query parameters
    dataset_name = "test"
    table_name = ""
    ai_model = "gemini"

    # Validate input parameters
    if not dataset_name:
        return {"error": "dataset_name is required"}, 400

    # Initialize handlers
    bigquery_handler = BigQueryHandler()
    cloud_storage_handler = CloudStorageHandler()

    if not ai_model:
        print("Testing ChatGPT helper...")
        try:
            table_sample = bigquery_handler.fetch_table_rows(dataset_name, table_name)
            chatgpt_result = generate_chatgpt_description(table_sample)
            print("ChatGPT Description:\n", chatgpt_result)
        except Exception as e:
            print("ChatGPT Test Failed:", e)

        print("\nTesting Gemini helper...")
        try:
            table_sample = bigquery_handler.fetch_table_rows(dataset_name, table_name)
            gemini_result = generate_gemini_description(table_sample)
            print("Gemini Description:\n", gemini_result)
        except Exception as e:
            print("Gemini Test Failed:", e)
        return {"status": "successfully generated both discriptions"}, 200

    # If table_name is provided, process a single table
    if table_name:
        table_sample = bigquery_handler.fetch_table_rows(dataset_name, table_name)
        #print(table_sample)
        ai_response = generate_ai_descriptions(table_sample, ai_model)
        print("Discription Generated properly...")
        cloud_storage_handler.save_to_bucket(dataset_name, table_name, ai_response)
        return {"status": "success", "description": ai_response}, 200

    # If table_name is not provided, process all tables in the dataset
    table_list = bigquery_handler.list_tables_in_dataset(dataset_name)
    print("----------TABLE LIST---------",table_list)
    results = []
    for table_name in table_list:
        print("----------TABLE LIST---------",table_name)
        table_sample = bigquery_handler.fetch_table_rows(dataset_name, table_name)
        ai_response = generate_ai_descriptions(table_sample, ai_model)
        cloud_storage_handler.save_to_bucket(dataset_name, table_name, ai_response)
        results.append({
            "table_name": table_name,
            "description": ai_response
        })

    return {"status": "success", "results": results}, 200


if __name__ == "__main__":
    process_dataset_main()