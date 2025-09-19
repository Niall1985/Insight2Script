import asyncio
from langgraph.graph import StateGraph, END, START
from typing import TypedDict
from trends_tool.news_tool import get_news_articles_count
from trends_tool.search_tool import get_web_total_results
from trends_tool.yt_tool import yt_tool_main
from trends_agent.agent import llm


class TrendState(TypedDict):
    topic: str
    news_count: int
    search_count: int
    yt_data: list


def fetch_news(state: TrendState):
    topic = state["topic"]
    return {"news_count": get_news_articles_count(topic)}

def fetch_search(state: TrendState):
    topic = state["topic"]
    return {"search_count": get_web_total_results(topic)}

def fetch_youtube(state: TrendState):
    topic = state["topic"]
    return {"yt_data": yt_tool_main(topic)}



builder = StateGraph(TrendState)

builder.add_node("news", fetch_news)
builder.add_node("search", fetch_search)
builder.add_node("youtube", fetch_youtube)


builder.add_edge("news", END)
builder.add_edge("search", END)
builder.add_edge("youtube", END)


builder.add_edge(START, "news")
builder.add_edge(START, "search")
builder.add_edge(START, "youtube")

graph = builder.compile()


async def run_trend_analysis(topic: str) -> dict:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, graph.invoke, {"topic": topic})
    llm_res = llm(result)  
    return llm_res


def get_trend_data(topic: str) -> dict:
    """Sync wrapper to call async run_trend_analysis."""
    return asyncio.run(run_trend_analysis(topic))



# if __name__ == "__main__":
#     topic = "Stephen Hawking"
#     final_result = get_trend_data(topic)
#     print(final_result)
