from langgraph.graph import START, StateGraph, END
from research_tools.ddg_tool import extract_ddg_results
from research_tools.wiki_tool import extract_wiki_data
from research_tools.serp_tool import get_youtube_links
from typing import TypedDict
import asyncio

class NodeData(TypedDict):
    query: str
    ddg_results: list
    wiki_results: list
    youtube_results: list

# Wrapper functions that extract query from state
def ddg_search_node(state: NodeData) -> NodeData:
    query = state["query"]
    results = extract_ddg_results(query)
    return {"ddg_results": results}

def wiki_search_node(state: NodeData) -> NodeData:
    query = state["query"]
    results = extract_wiki_data(query)
    return {"wiki_results": results}

def youtube_search_node(state: NodeData) -> NodeData:
    query = state["query"]
    results = get_youtube_links(query)
    return {"youtube_results": results}

builder = StateGraph(NodeData)

# Add nodes with wrapper functions
builder.add_node("wikipedia_search", wiki_search_node)
builder.add_node("ddg_search", ddg_search_node)
builder.add_node("youtube_search", youtube_search_node)

# Add edges using the string identifiers
builder.add_edge(START, "wikipedia_search")
builder.add_edge(START, "ddg_search")
builder.add_edge(START, "youtube_search")

builder.add_edge("wikipedia_search", END)
builder.add_edge("ddg_search", END)
builder.add_edge("youtube_search", END)

# Compile the graph
graph = builder.compile()

async def main():
    # Provide initial state with query
    initial_state = {
        "query": "Nikola Tesla",
        "ddg_results": [],
        "wiki_results": [],
        "youtube_results": []
    }
    results = await graph.ainvoke(initial_state)
    print("Final results:", results)

if __name__ == "__main__":
    asyncio.run(main())


