from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm1 = ChatGroq(groq_api_key = os.getenv('groq_key1'), model_name = "llama-3.1-8b-instant") #wiki content summarization
llm2 = ChatGroq(groq_api_key = os.getenv('groq_key2'), model_name = "llama-3.1-8b-instant") #fetch important urls
llm3 = ChatGroq(groq_api_key = os.getenv('groq_key3'), model_name = "llama-3.1-8b-instant") #summarize scraped content from reduced urls