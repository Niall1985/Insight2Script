from langgraph.graph import START, StateGraph, END
from research_tools.ddg_tool import extract_ddg_results
from research_tools.wiki_tool import extract_wiki_data
from research_tools.serp_tool import get_youtube_links
from typing import TypedDict
import asyncio
import json
from dotenv import load_dotenv
import os
from research_agent.agent import runagent
load_dotenv()

file_path = os.getenv('file_path')
class NodeData(TypedDict):
    query: str
    ddg_results: str
    wiki_results: str
    youtube_results: str

def ddg_search_node(state: NodeData) -> dict:
    query = state["query"]
    results = extract_ddg_results(query)
    return {"ddg_results": results}


def wiki_search_node(state: NodeData) -> dict:
    query = state["query"]
    results = extract_wiki_data(query)
    return {"wiki_results": results}


def youtube_search_node(state: NodeData) -> dict:
    query = state["query"]
    results = get_youtube_links(query)
    return {"youtube_results": results}


builder = StateGraph(NodeData)

builder.add_node("wikipedia_search", wiki_search_node)
builder.add_node("ddg_search", ddg_search_node)
builder.add_node("youtube_search", youtube_search_node)

builder.add_edge(START, "wikipedia_search")
builder.add_edge(START, "ddg_search")
builder.add_edge(START, "youtube_search")

builder.add_edge("wikipedia_search", END)
builder.add_edge("ddg_search", END)
builder.add_edge("youtube_search", END)

graph = builder.compile()

async def main():
    
    initial_state = {
        "query": "Nikola Tesla",
        "ddg_results": "",
        "wiki_results": "",
        "youtube_results": ""
    }
    results = await graph.ainvoke(initial_state)
    with open("results.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(results, indent=4))

if __name__ == "__main__":
    async def combined():
        
        await main()  

        await runagent(file_path)
    
    asyncio.run(combined())



