import streamlit as st
import os
from dotenv import load_dotenv
import time
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import threading
import openai
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries"),
    ("user", "{question}")
])

llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

class RateLimitedAPI:
    def __init__(self):
        self.lock = threading.Lock()
        self.last_call_time = time.time()
        self.max_calls_per_minute = 60  # Adjust based on your quota

    def check_rate_limit(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        if elapsed_time < 60:
            remaining_calls = int(60 - elapsed_time) + 1
            print(f"Rate limit warning: {remaining_calls} seconds until next call allowed.")
            return False
        else:
            self.last_call_time = current_time
            return True

    def safe_call(self, func):
        with self.lock:
            if not self.check_rate_limit():
                print("Rate limit exceeded. Waiting...")
                time.sleep(61)  # Wait slightly longer than the maximum allowed time
                return self.safe_call(func)

            try:
                return func()
            except openai.RateLimitError as e:
                print(f"Rate limit exceeded. Error: {e}")
                time.sleep(61)  # Wait slightly longer than the maximum allowed time
                return self.safe_call(func)

rate_limited_api = RateLimitedAPI()

def generate_response(input_text):
    chain = prompt | llm | output_parser
    return chain.invoke({'question': input_text})

if st.button('Generate Response'):
    st.write(rate_limited_api.safe_call(generate_response))
