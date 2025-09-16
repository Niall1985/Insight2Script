from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph, END
from typing import TypedDict
import asyncio
import json
import os

load_dotenv()

# file_path = os.getenv('file_path')
llm1 = ChatGroq(groq_api_key=os.getenv('groq_key1'), model_name="llama-3.1-8b-instant")
llm2 = ChatGroq(groq_api_key=os.getenv('groq_key2'), model_name="llama-3.1-8b-instant")
llm3 = ChatGroq(groq_api_key=os.getenv('groq_key3'), model_name="llama-3.1-8b-instant")

class NodeData(TypedDict):
    query: str
    ddg_results: str
    wiki_results: str
    youtube_results: str
    ddg_summary: list
    wiki_summary: list
    youtube_summary: list

def chunk_text(text, chunk_size=1000, overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    return splitter.split_text(text)

def call_llm(llm, chunks, prompt_template_str):
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template=prompt_template_str
    )
    results = []
    for chunk in chunks:
        prompt = prompt_template.format(text=chunk)
        results.append(llm(prompt))
    return results

def ddg_summarize_node(state: NodeData) -> dict:
    text = state["ddg_results"]
    chunks = chunk_text(text)
    prompt = "Summarize the following DuckDuckGo search results:\n\n{text}"
    summary = call_llm(llm1, chunks, prompt)
    return {"ddg_summary": summary}

def wiki_summarize_node(state: NodeData) -> dict:
    text = state["wiki_results"]
    chunks = chunk_text(text)
    prompt = "Summarize the following Wikipedia content:\n\n{text}"
    summary = call_llm(llm2, chunks, prompt)
    return {"wiki_summary": summary}

def youtube_summarize_node(state: NodeData) -> dict:
    text = state["youtube_results"]
    chunks = chunk_text(text)
    prompt = "Summarize the following YouTube transcript:\n\n{text}"
    summary = call_llm(llm3, chunks, prompt)
    return {"youtube_summary": summary}

builder = StateGraph(NodeData)

builder.add_node("ddg_summarize", ddg_summarize_node)
builder.add_node("wiki_summarize", wiki_summarize_node)
builder.add_node("youtube_summarize", youtube_summarize_node)

builder.add_edge(START, "ddg_summarize")
builder.add_edge(START, "wiki_summarize")
builder.add_edge(START, "youtube_summarize")

builder.add_edge("ddg_summarize", END)
builder.add_edge("wiki_summarize", END)
builder.add_edge("youtube_summarize", END)

graph = builder.compile()

def ddg_res(file_path): 
    with open(file_path, "r" ,encoding='utf-8') as file: 
        data = json.load(file) 
        ddg_content = data.get("ddg_results", "") 
    return ddg_content 

def wiki_res(file_path): 
    with open(file_path, "r" ,encoding='utf-8') as file: 
        data = json.load(file) 
        wiki_content = data.get("wiki_results", "") 
    return wiki_content 

def yt_res(file_path): 
    with open(file_path, "r" ,encoding='utf-8') as file: 
        data = json.load(file) 
        yt_content = data.get("youtube_results", "") 
    return yt_content

async def runagent(file_path):
    initial_state = {
        "query": "Nikola Tesla",
        "ddg_results": ddg_res(file_path),
        "wiki_results": wiki_res(file_path),
        "youtube_results": yt_res(file_path),
        "ddg_summary": [],
        "wiki_summary": [],
        "youtube_summary": []
    }
    
    results = await graph.ainvoke(initial_state)

    with open("summaries.json", "w", encoding='utf-8') as file:
        json.dump(results, file, indent=4)

# if __name__ == "__main__":
#     asyncio.run(runagent())
