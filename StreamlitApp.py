import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file, get_table_data,jsonParser
import streamlit as st
from src.mcq_generator.logger import logging
from src.mcq_generator.MCQGenerator import generate_evaluate_chain

with open(r"C:\Users\Harsh_Kr\OneDrive\Desktop\GenAI\mcqgen\Responce.json", "r") as f:
    RESPONSE_JSON = f.read()
    
st.title("MCQ Generator Application")

with st.form("user_inputs"):
    upload_file = st.file_uploader("Upload your file", type=["pdf", "txt"])
    
    mcq_count = st.number_input("Number of MCQs to generate", min_value=1, max_value=20, value=2)
    
    subject = st.text_input("Subject", max_chars=50)
    
    tone = st.text_input("Complexity level", max_chars=50, placeholder="e.g., Formal, Informal, Humorous, simple")
    
    button = st.form_submit_button("Generate MCQs") 
    
    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text=read_file(upload_file)
                
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
                
            except Exception as e:
                traceback.print_exception(type(e), value=e, tb=e.__traceback__)
                st.error(f"An error occurred: {e}")
                
            else:
                print('cost : haha 1 million dollar')
                quiz = jsonParser(response.get('quiz'))
                # st.write(quiz)  
                if quiz is not None:
                    df = get_table_data(quiz)
                    st.table(df)
                    df.index = df.index + 1
                    st.text_area(label="Review", value=response['review'], height=200)
                    
                        
                        