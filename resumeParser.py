from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage,SystemMessage, HumanMessage, ToolMessage, AIMessage
from typing_extensions import TypedDict, Annotated, Literal
import operator
from dotenv import load_dotenv
load_dotenv() 

chatModel = init_chat_model("gpt-4o-mini")

class resumeDetails(TypedDict):
    role: str
    seniority: str
    skills: list[str]
    expereince: str
    stregths: list[str]
    weaknesses: list[str]
    achievements: list[str]
    education: list[str]
    certifications: list[str]
    projects: list[str]

class ResumeParseState(TypedDict):
    resume_Praser: str
    resume_details: resumeDetails
    resumeRating: int
    llm_calls: int
    summary: str
    messages: Annotated[list[BaseMessage], operator.add]


def profilePrase(state: ResumeParseState):
    pass

def getResumeDetailAndRating(state: ResumeParseState):
    pass

def resumeChatBot(state: ResumeParseState):
    pass

def generateSummary(state: ResumeParseState):
    pass

def checkIfDone(state: ResumeParseState) -> Literal["resumeChatBot", "generateSummary"]:
    return "generateSummary"


graph = StateGraph(ResumeParseState)

graph.add_node("ProfilePrase", profilePrase)
graph.add_node("getResumeDetailAndRating", getResumeDetailAndRating)
graph.add_node("resumeChatBot", resumeChatBot)
graph.add_node("generateSummary", generateSummary)

graph.add_edge(START, "ProfilePrase")
graph.add_edge("ProfilePrase", "getResumeDetailAndRating")
graph.add_conditional_edges("resumeChatBot", checkIfDone,["resumeChatBot", "generateSummary"])

graph.add_edge("generateSummary", END)

agent = graph.compile()

agent.invoke({})
