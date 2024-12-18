import sys
import os

# Add the parent directory (root of the repo) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import functions_framework
from flask import jsonify
from app import process_tables

@functions_framework.http
def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    #return "Hello World!"
    request_json = request.get_json()
    #request_json = headers["content-type"]

    # Check if the request body is valid and contains 'dataset_name' and 'table_name'
    if not request_json:
        return jsonify({'error': 'No JSON body provided'}), 400
    
    dataset_name = request_json.get('dataset_name')
    table_name = request_json.get('table_name')
    row_no = request_json.get('rows_sample')

    # Validate if dataset_name is provided and not empty
    if not dataset_name:
        return jsonify({'error': 'The parameter "dataset_name" is required and cannot be empty'}), 400
    
    # Validate if table_name is provided and not empty
    if not table_name:
        return jsonify({'error': 'The parameter "table_name" is required and cannot be empty'}), 400


    # Validate that dataset_name and table_name are not numbers
    if dataset_name.isdigit():
        return jsonify({'error': 'The parameter "dataset_name" cannot be a number'}), 400
    
    if table_name.isdigit():
        return jsonify({'error': 'The parameter "table_name" cannot be a number'}), 400

    # Validate that rows_sample is a number and not a letter
    if isinstance(row_no, str) and row_no.isalpha():
        return jsonify({'error': 'The parameter "rows_sample" cannot be a letter'}), 400

    # Ensure that rows_sample is a valid integer and greater than or equal to 1
    try:
        row_no = int(row_no)
        if row_no < 1:
            return jsonify({'error': 'The parameter "rows_sample" must be greater than or equal to 1'}), 400
    except ValueError:
        return jsonify({'error': 'The parameter "rows_sample" must be a valid integer'}), 400

    

    # If both parameters are valid, return a success message
    """return jsonify({
        'message': 'Parameters received successfully!',
        'dataset_name': dataset_name,
        'table_name': table_name,
        'rows_sample' : row_no
    })"""

    result = process_tables(dataset_name, table_name, row_no)

    # Return the result of processing
    return jsonify(result)

if __name__ == "__main__":
     print("Helloooooo")
