from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage,SystemMessage, HumanMessage, ToolMessage, AIMessage
from typing_extensions import TypedDict, Annotated, Literal
import operator
from pypdf import PdfReader
from dotenv import load_dotenv
load_dotenv() 

chatModel = init_chat_model("gpt-4o-mini")

class ResumeDetails(TypedDict):
    role: str
    seniority: str
    skills: list[str]
    experience: str
    stregths: list[str]
    weaknesses: list[str]
    achievements: list[str]
    education: list[str]
    certifications: list[str]
    projects: list[str]

class ResumeParseState(TypedDict):
    resume_Praser: str
    resume_details: ResumeDetails
    resumeRating: int
    llm_calls: int
    summary: str
    messages: Annotated[list[BaseMessage], operator.add]


def profilePrase(state: ResumeParseState):
        try:
            reader = PdfReader("./linkedinPdf/rupesh_profile.pdf")
            resume_Praser = "\n".join(page.extract_text() for page in reader.pages )
            return {"resume_Praser": resume_Praser}
        except Exception as e:
            print("Error reading PDF:", e)
            return {"resume_Praser": ""}


def getResumeDetailAndRating(state: ResumeParseState):
        try:
            prompt = ChatPromptTemplate.from_template("""Use below content to extract resume details such as role, seniority, skills, experience, strengths, weaknesses, achievements, education, certifications, and projects.
            Provide the details in a structured format.

            Context:
            {resume_Praser}
            """)
            model_with_structure = chatModel.with_structured_output(ResumeDetails)
            chain = prompt | model_with_structure
            resume_details = chain.invoke({"resume_Praser": state["resume_Praser"]})
            print("Extracted Resume Details: ===> ", resume_details)
            return {"resume_details": resume_details}
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return {"resume_details": []}

def resumeChatBot(state: ResumeParseState):
        print("resumeChatBot ===> ")

def generateSummary(state: ResumeParseState):
        print("generateSummary ===> ")


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
