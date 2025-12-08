import os
import json
import traceback
import PyPDF2
import re
import pandas as pd


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("error reading the PDF file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
        )
        
        
# def get_table_data(quiz_str):
#     try:
#         # convert the quiz from a str to dict
#         quiz_dict = json.loads(quiz_str)
#         quiz_table_data = []

#         # iterate over the quiz dictionary and extract the required information
#         for key, value in quiz_dict.items():
#             mcq = value['mcq']
#             options = " || ".join(
#                 f"{option} -> {option_value}" for option, option_value in value["options"].items()
#             )
#             correct = value['correct']
#             quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

#         return quiz_table_data

#     except Exception as e:
#         traceback.print_exception(type(e), e, e.__traceback__)
#         return False
    
    
    
def get_table_data(quiz_dict) :

    # 1. Load the JSON string into a Python dictionary
    # try:
    #     quiz_dict = json.loads(quiz_json_str)
    # except json.JSONDecodeError as e:
    #     print(f"Error decoding JSON: {e}")
    #     return pd.DataFrame()

    data_list = []

    # 2. Iterate through the dictionary to extract and format data
    for q_num_str, q_data in quiz_dict.items():
        row = {
            "Question Number": int(q_num_str),
            "Question": q_data.get("mcq"),
            "Answer": q_data.get("correct"),
        }
        
        # 3. Extract all options (a, b, c, d)
        options = q_data.get("options", {})
        
        # Add options to the row, using None/NaN if an option key is missing
        row['a'] = options.get('a')
        row['b'] = options.get('b')
        row['c'] = options.get('c')
        row['d'] = options.get('d')

        data_list.append(row)

    # 4. Create the DataFrame and reorder columns
    df = pd.DataFrame(data_list)
    
    # Ensure all required columns exist and are in the correct order
    column_order = [
        "Question Number", 
        "Question", 
        "a", 
        "b", 
        "c", 
        "d", 
        "Answer"
    ]
    
    # Select and return the final DataFrame with the desired column order
    return df


def jsonParser(quiz):
    
    clean_output = quiz.strip("'")
    match = re.search(r"```json\s*(.*?)\s*```", clean_output, re.DOTALL)

    if match:
        json_string = match.group(1).strip()
        
        try:
            data = json.loads(json_string)
            print("JSON loaded successfully into a Python dictionary.")
            return data
            
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode the cleaned JSON string: {e}")
            print("--- Problematic String ---")
            print(json_string)
            return json_string
            
    else:
        print("Error: Could not find '```json' or the closing '```' in the output.")
    