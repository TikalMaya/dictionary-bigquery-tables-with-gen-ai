import pandas as pd
from ai_agent import generate_chatgpt_description, generate_gemini_description

def test_ai_helpers():
    """
    Function to test AI helper functions (ChatGPT and Gemini).
    """
    # Sample table data (mimics what a BigQuery table might look like)
    table_sample = pd.DataFrame({
        "column1": [1, 2, 3, 4, 5],
        "column2": ["a", "b", "c", "d", "e"],
        "column3": [True, False, True, False, True]
    })

    print("Testing ChatGPT helper...")
    try:
        chatgpt_result = generate_chatgpt_description(table_sample)
        print("ChatGPT Description:\n", chatgpt_result)
    except Exception as e:
        print("ChatGPT Test Failed:", e)

    print("\nTesting Gemini helper...")
    try:
        gemini_result = generate_gemini_description(table_sample)
        print("Gemini Description:\n", gemini_result)
    except Exception as e:
        print("Gemini Test Failed:", e)


if __name__ == "__main__":
    # Run the test function
    test_ai_helpers()
