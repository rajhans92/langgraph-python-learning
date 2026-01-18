from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict, total=False):
    analysis: str
    headline: str
    experience: str
    validated: bool

def input_data(state: State):
    return state

def planner(state: State) -> str:
    if "analysis" not in state:
        return "analyze"
    if "headline" not in state:
        return "improve_headline"
    if "experience" not in state:
        return "improve_experience"
    return "validate"

def analyze(state: State):
    state["analysis"] = "Profile analysis done"
    return state

def improve_headline(state: State):
    state["headline"] = "Improved LinkedIn headline"
    return state

def improve_experience(state: State):
    state["experience"] = "Improved experience section"
    return state

def validate(state: State):
    state["validated"] = True
    print("Profile improvement completed")
    return state

graph = StateGraph(State)

graph.add_node("input_data", input_data)
graph.add_node("analyze", analyze)
graph.add_node("improve_headline", improve_headline)
graph.add_node("improve_experience", improve_experience)
graph.add_node("validate", validate)

graph.add_edge(START, "input_data")
graph.add_conditional_edges("input_data", planner, ["analyze", "improve_headline", "improve_experience", "validate"])
graph.add_edge("analyze", "input_data")
graph.add_edge("improve_headline", "input_data")
graph.add_edge("improve_experience", "input_data")
graph.add_edge("validate", END)

checkpoint_saver = InMemorySaver()
agent = graph.compile(checkpointer=checkpoint_saver)
config = {"configurable":{"thread_id": "1"}}
result = agent.invoke({},config)
print("Final State:", result)
print(list(agent.get_state(config)))