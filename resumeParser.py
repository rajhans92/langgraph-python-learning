from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage,SystemMessage, HumanMessage, ToolMessage, AIMessage
from typing_extensions import TypedDict, Annotated, Literal
import operator
from pypdf import PdfReader
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
        reader = PdfReader("./linkedinPdf/rupesh_profile.pdf")
        resume_Praser = "\n".join(page.extract_text() for page in reader.pages )
        # print(resume_Praser)
        return {"resume_Praser": resume_Praser}


def getResumeDetailAndRating(state: ResumeParseState):
        print("getResumeDetailAndRating ===> ")
        return {
            "resume_details": {
                "role": "Software Engineer",
                "seniority": "Mid-level",
                "skills": ["Python", "Java", "SQL"],
                "expereince": "5 years",
                "stregths": ["Problem-solving", "Teamwork"],
                "weaknesses": ["Public speaking"],
                "achievements": ["Employee of the Month"],
                "education": ["B.Sc. in Computer Science"],
                "certifications": ["AWS Certified Developer"],
                "projects": ["E-commerce Website", "Mobile App Development"]
            }}

def resumeChatBot(state: ResumeParseState):
        print("resumeChatBot ===> ",state)

def generateSummary(state: ResumeParseState):
        print("generateSummary ===> ",state)


def checkIfDone(state: ResumeParseState) -> Literal["resumeChatBot", "generateSummary"]:
    return "generateSummary"


graph = StateGraph(ResumeParseState)

graph.add_node("ProfilePrase", profilePrase)
graph.add_node("getResumeDetailAndRating", getResumeDetailAndRating)
graph.add_node("resumeChatBot", resumeChatBot)
graph.add_node("generateSummary", generateSummary)

graph.add_edge(START, "ProfilePrase")
graph.add_edge("ProfilePrase", "getResumeDetailAndRating")
graph.add_edge("getResumeDetailAndRating", "resumeChatBot")
graph.add_conditional_edges("resumeChatBot", checkIfDone,["resumeChatBot", "generateSummary"])

graph.add_edge("generateSummary", END)

agent = graph.compile()

agent.invoke({})
