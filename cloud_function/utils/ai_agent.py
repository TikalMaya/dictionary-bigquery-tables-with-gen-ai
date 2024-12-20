import os # for environment variables
import json
from openai import OpenAI
import google.generativeai as genai
from api_key_manager import get_api_key


print("Loading ChatGPT client... with OpenAI api_key:", get_api_key("chatgpt"))
print("Loading Gemini client... with OpenAI api_key:", get_api_key("gemini"))
client = OpenAI(
    api_key=get_api_key("chatgpt")  # This is the default and can be omitted
)

genai.configure(api_key=get_api_key("gemini"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')


def generate_chatgpt_description(table_sample):
    """
    Generates a description using ChatGPT.
    """
    prompt = create_prompt(table_sample)
    response = client.chat.completions.create(
        model="gpt-4o", # use the latest model
        messages=[{"role": "system", "content": 'Eres un experto analista de datos y generador de descripciones que domina el español.'}, {"role": "user", "content": prompt}],
    )
    # Extract the generated message content
    content = response.choices[0].message.content.strip()
    content = content.replace("```json","").replace("```","")
    return json.loads(content)


def generate_gemini_description(table_sample, api_key = None):
    """
    Generates a description using Gemini.
    """
    prompt = create_prompt(table_sample)
    
    if api_key == None:
      api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("Gemini API key not found. Set 'GEMINI_API_KEY' environment variable or pass directly to function.")
    
    response = model.generate_content(prompt)
    
    try:
        # Extract content, remove backticks, and load as JSON
        content = response.text.strip()
        #remove backticks from response
        content = content.replace("```json","").replace("```","")
        return json.loads(content)
    except json.JSONDecodeError:
        print("Error: Gemini output is not valid JSON.")
        print("Response text:", response.text)
        return None

    """
    Creates a prompt for Gemini to generate descriptions in English (as you specified).
    """
    prompt = f"""
        Objective: Your task is to analyze the column names and provide descriptions for each one.
        Do not provide speculative answers.
        By description, we want a clear understanding of the column's purpose or function. **Do not include** examples from the column's data or the data type it contains.
        Columns to document:

        {table_sample.head().to_dict()}

        Table content:
        {table_sample.to_string()}

        Guidelines:
            1 - Analyze the table and classify it within a context.
            2 - With the context defined, analyze the data and the column name, and create a **complete description** for each column.
            3 - **Do not expose the column's content in the description**, not even to exemplify, and it's also not necessary to expose data types.
            4 - **Return the description in JSON format**

        Expected Output:

        {{
            "Column_Name": "Description",
            "Column_Name": "Description"
            ...
        }}

        """
    return prompt

def create_prompt(table_sample):
    """
    Creates a prompt for ChatGPT to generate descriptions in Spanish.
    """
    prompt = f"""
        Objetivo: Sua tarefa é analisar os nomes das colunas e fornecer descrições para cada um delas. 
        no proporciones respuestas supuestas.
        Por descrição, queremos um entendimento claro da finalidade ou função da coluna. **Não inclua** exemplos dos dados na coluna ou o tipo de dados que ela contém."
        
        Colunas para documentar:

        {table_sample.head().to_dict()}

        Conteúdo da tabela:
        {table_sample.to_string()}

        Orientações:
            1 - Analise a tabela, e classifique-a dentro de um contexto.
            2 - Com o contexto definido, analise os dados e o nome da coluna, e crie uma **descrição completa** para cada coluna.
            3 - **Não exponha conteúdo da coluna na descrição**, nem mesmo para exemplificar, também não é necessário expor data types dos dados.
            4 - **Retorne a descrição em inglês**
            5 - **Retorne a descrição em formato JSON**
            6 - **Não inclua exemplos dos dados na descrição**
            7 - **mantener es breve y preciso**
            8 - **no incluya referencias a columnas actuales como esta columna de la columna actual**

        Resultado esperado:

        {{
            "Column_Name": "Description",
            "Column_Name": "Description"
            ...
        }}

        """
    return prompt
