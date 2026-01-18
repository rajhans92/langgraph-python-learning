from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from typing_extensions import TypedDict, Literal,Annotated
import operator
import dotenv
dotenv.load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

class CalcState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    result: int   

toolSet = [add, multiply]
model = init_chat_model("gpt-4o-mini").bind_tools(toolSet)
tool_node = ToolNode(toolSet)



def llmCall(state: CalcState):
    messages = model.invoke(state['messages'])
    return {
        "messages": [messages]
    }

def router(state: CalcState) -> Literal["tool_node", END]:
    last_response = state["messages"][-1]

    if last_response.tool_calls:
        return "tool_node"

    return END



graph = StateGraph(CalcState)

graph.add_node("llmCall", llmCall)
graph.add_node("tool_node", tool_node)

graph.add_edge(START, "llmCall")
graph.add_conditional_edges("llmCall", router, ["tool_node", END])
graph.add_edge("tool_node", "llmCall")

agent = graph.compile()
initial_state = {
    "messages": [
        HumanMessage(content="Multiply 4 and 5")
    ]
}
result = agent.invoke(initial_state)
# print("Final Result:", result)


