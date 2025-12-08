import os
import json
import re
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file, get_table_data 
from src.mcq_generator.logger import logging


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_classic.chains import SequentialChain

# loading env file 
load_dotenv()
API_KEY=os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", 
    temperature=0.4,
    google_api_key=API_KEY
)

# template 

TEMPLATE="""
Text:{text}

You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs

### RESPONSE_JSON
{response_json}

"""

quiz_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=TEMPLATE
)

quiz_chain = LLMChain(
    llm=llm,
    prompt=quiz_prompt,
    output_key="quiz",
    verbose=True
)


# to evaluate the quiz 
TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity \
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student \
Quiz_MCQs: 
{quiz}

Check from an expert English Writer of the above quiz:
"""


quiz_eval_prompt = PromptTemplate(
    input_variables=["quiz","subject"],
    template=TEMPLATE2
)

review_chain = LLMChain(
    llm=llm,
    prompt=quiz_eval_prompt,
    output_key="review",
    verbose=True
)


generate_evaluate_chain= SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text","number","subject","tone","response_json"],
    output_variables=["quiz","review"], 
    verbose=True
)