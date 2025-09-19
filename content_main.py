from langgraph.graph import START, StateGraph, END
from research_tools.ddg_tool import extract_ddg_results
from research_tools.wiki_tool import extract_wiki_data
from research_tools.serp_tool import get_youtube_links
from typing import TypedDict
import asyncio
import json
from dotenv import load_dotenv
import os
from research_agent.intermediate_summarizer import ddg_summarizer_func, wiki_summarizer_func, yt_summarizer_func
from research_agent.agent import runagent
from query_processor.query_agent import query_processing_agent
from content_generator.content_agent import content_llm
load_dotenv()

# ddg_summary = None
# wiki_summary = None
# youtube_summary = None

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

async def main(query):
    
    initial_state = {
    "query": query,
    "ddg_results": "",
    "wiki_results": "",
    "youtube_results": ""
    }

    results = await graph.ainvoke(initial_state)

    ddg_results = results.get("ddg_results", "")
    wiki_results = results.get("wiki_results", "")
    youtube_results = results.get("youtube_results", "")

    ddg_summary = ddg_summarizer_func(ddg_results)
    wiki_summary = wiki_summarizer_func(wiki_results)
    youtube_summary = yt_summarizer_func(youtube_results)

    return ddg_summary, wiki_summary, youtube_summary


# if __name__ == "__main__":
#     async def combined(input_query):
        
#         ddg_summary, wiki_summary, youtube_summary = await main(input_query)  

#         ddg_summary_final, wiki_summary_final, youtube_summary_final = await runagent(ddg_summary, wiki_summary, youtube_summary)
#         print(ddg_summary_final)
#         print(wiki_summary_final)
#         print(youtube_summary_final)

#     input_query = input("Enter your prompt: ")
#     asyncio.run(combined(input_query))


async def combined(input_query):
    ddg_results, wiki_results, youtube_results = await main(input_query)  

    ddg_summary, wiki_summary, youtube_summary = await runagent(ddg_results, wiki_results, youtube_results)

    print("\n=== DuckDuckGo Summary ===")
    print(ddg_summary)

    print("\n=== Wikipedia Summary ===")
    print(wiki_summary)

    print("\n=== YouTube Summary ===")
    print(youtube_summary)

    script = content_llm(ddg_summary, wiki_summary, youtube_summary)
        
    print("\n=== Video Script ===")
    print(script)
    return script

# input_query = input("Enter your prompt: ")
# formatted_query = query_processing_agent(input_query)
# print(formatted_query)
# asyncio.run(combined(formatted_query))


