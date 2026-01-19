from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
load_dotenv()

# Ensure you have set your Tavily API key as an environment variable

# Define subgraph
class SubgraphState(TypedDict):
    query: str
    search_results: str

def tavily_search(state: SubgraphState):
    search = TavilySearchResults(max_results=1)
    results = search.invoke(state["query"])
    return {"search_results": results}

def process_results(state: SubgraphState):
    search_results = state["search_results"]
    processed_result = ""

    if isinstance(search_results, list):
        for result in search_results:
            url = result.get("url", "No URL")
            content = result.get("content", "No Content")

            processed_result += f"URL: {url}\nContent: {content}...\n\n"  #Added the url to the process result
    else:
        processed_result = "No search results found."

    return {"query": state["query"] + " - " + processed_result}

subgraph = StateGraph(SubgraphState)
subgraph.add_node("search", tavily_search)
subgraph.add_node("process", process_results)
subgraph.add_edge(START, "search")
subgraph.add_edge("search", "process")

subgraph = subgraph.compile()

# Define parent graph
class ParentState(TypedDict):
    query: str

def node_1(state: ParentState):
    return {"query": "Searching for: " + state["query"]}

def node_2(state: ParentState):
    # transform the state to the subgraph state
    response = subgraph.invoke({"query": state["query"]})
    # transform response back to the parent state
    return {"search_results": response["search_results"]}

builder = StateGraph(ParentState)
builder.add_node("node_1", node_1)
builder.add_node("subgraph", subgraph)  # Add the compiled subgraph as a node
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "subgraph")
builder.add_edge("subgraph", END)

graph = builder.compile()


image = graph.get_graph().draw_ascii()
print(image)
image1 =graph.get_graph().draw_png()

with open("sreeni_Main_and_subgraph_as_node.png","wb") as file:
    file.write(image1)
# Run the graph
result= graph.invoke({"query": "NVIDA"}, subgraphs=True)
print(result)