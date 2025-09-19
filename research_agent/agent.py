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

llm1 = ChatGroq(groq_api_key=os.getenv('groq_key1'), model_name="llama-3.1-8b-instant")
llm2 = ChatGroq(groq_api_key=os.getenv('groq_key2'), model_name="llama-3.1-8b-instant")
llm3 = ChatGroq(groq_api_key=os.getenv('groq_key3'), model_name="llama-3.1-8b-instant")

class NodeData(TypedDict):
    query: str
    ddg_results: str
    wiki_results: str
    youtube_results: str
    ddg_summary_final: str
    wiki_summary_final: str
    youtube_summary_final: str

def call_llm(llm, text, prompt_template_str) -> str:
    if not text.strip():
        return ""
    prompt = PromptTemplate(input_variables=["text"], template=prompt_template_str).format(text=text)
    response = llm.invoke(prompt)
    return response.content

def ddg_final_summarize_node(state: NodeData) -> dict:
    text = state["ddg_results"]
    prompt = f"Further summarize these DuckDuckGo results into 2-3 concise sentences:\n\n{text}"
    summary = call_llm(llm1, text, prompt)
    return {"ddg_summary_final": summary}

def wiki_final_summarize_node(state: NodeData) -> dict:
    text = state["wiki_results"]
    prompt = f"Further summarize this Wikipedia content into 2-3 concise sentences:\n\n{text}"
    summary = call_llm(llm2, text, prompt)
    return {"wiki_summary_final": summary}

def youtube_final_summarize_node(state: NodeData) -> dict:
    text = state["youtube_results"]
    prompt = f"Further summarize this YouTube transcript into 2-3 concise sentences:\n\n{text}"
    summary = call_llm(llm3, text, prompt)
    return {"youtube_summary_final": summary}

builder = StateGraph(NodeData)

builder.add_node("ddg_final", ddg_final_summarize_node)
builder.add_node("wiki_final", wiki_final_summarize_node)
builder.add_node("youtube_final", youtube_final_summarize_node)

builder.add_edge(START, "ddg_final")
builder.add_edge(START, "wiki_final")
builder.add_edge(START, "youtube_final")

builder.add_edge("ddg_final", END)
builder.add_edge("wiki_final", END)
builder.add_edge("youtube_final", END)

graph = builder.compile()

async def runagent(ddg_summary, wiki_summary, youtube_summary):
   
    initial_state = {
        "query": "Nikola Tesla",
        "ddg_results": ddg_summary,
        "wiki_results": wiki_summary,
        "youtube_results": youtube_summary,
        "ddg_summary_final": "",
        "wiki_summary_final": "",
        "youtube_summary_final": ""
    }

    results = await graph.ainvoke(initial_state)

    ddg_summary_final = results.get("ddg_summary_final", "")
    wiki_summary_final = results.get("wiki_summary_final", "")
    youtube_summary_final = results.get("youtube_summary_final", "")

    # with open("summaries.json", "w", encoding='utf-8') as file:
    #     json.dump(results, file, indent=4)

    return ddg_summary_final, wiki_summary_final, youtube_summary_final
