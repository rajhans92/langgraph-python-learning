from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class TravelState(TypedDict):
    city_name: str
    weather: str
    air_quality: str
    traffic_conditions: str
    travel_advisories: str
    summary_report: str

def input_data(state: TravelState):
    pass

def waether(state: TravelState):
    pass

def air_quality(state: TravelState):
    pass

def traffic_conditions(state: TravelState):
    pass

def travel_advisories(state: TravelState):
    pass

def summary_report(state: TravelState):
    pass

graph = StateGraph(TravelState)

graph.add_node("input_data", input_data)
graph.add_node("weather", waether)
graph.add_node("air_quality", air_quality)
graph.add_node("traffic_conditions", traffic_conditions)
graph.add_node("travel_advisories", travel_advisories)
graph.add_node("summary_report", summary_report)

graph.add_edge(START, "input_data")
graph.add_edge("input_data", "weather")
graph.add_edge("input_data", "air_quality")
graph.add_edge("input_data", "traffic_conditions")
graph.add_edge("input_data", "travel_advisories")
graph.add_edge("weather", "summary_report")
graph.add_edge("air_quality", "summary_report")
graph.add_edge("traffic_conditions", "summary_report")
graph.add_edge("travel_advisories", "summary_report")   
graph.add_edge("summary_report", END)

agent = graph.compile() 
result = agent.invoke({})