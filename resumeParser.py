from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage,SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import TypedDict, Annotated, Literal,List
from pydantic import BaseModel, Field
import operator
import json
from pypdf import PdfReader
from dotenv import load_dotenv
load_dotenv() 

chatModel = init_chat_model("gpt-4o-mini")

class ResumeDetails(BaseModel):
    role: str = Field(
        description="Primary job title or professional role of the candidate"
    )

    seniority: str = Field(
        description="Career level such as Junior, Mid-level, Senior, Lead, or Architect"
    )

    skills: List[str] = Field(
        description="List of technical and professional skills"
    )

    experience: str = Field(
        description="Summary of total experience and key responsibilities"
    )

    strengths: List[str] = Field(
        description="Key strengths of the candidate"
    )

    weaknesses: List[str] = Field(
        description="Areas where the candidate can improve"
    )

    achievements: List[str] = Field(
        description="Notable achievements with measurable impact"
    )

    education: List[str] = Field(
        description="Educational qualifications"
    )

    certifications: List[str] = Field(
        description="Professional certifications"
    )

    projects: List[str] = Field(
        description="Important projects with brief outcomes"
    )

    overallImpression: str = Field(
        description="High-level evaluation of the candidate's profile"
    )

    overallRating: int = Field(
        ge=1,
        le=10,
        description="Overall profile rating on a scale from 1 to 10"
    )

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
            return {"resume_details": resume_details}
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return {"resume_details": []}

def resumeChatBot(state: ResumeParseState):
        
        chatBotTemp = f""" You will receive the user's LinkedIn profile data in JSON format.
                        Your objectives are to:
                        - Evaluate clarity, impact, and keyword optimization.
                        - Identify gaps, redundancies, and weak phrasing.
                        - Suggest improvements aligned with industry best practices and ATS/recruiter expectations.

                        When the user provides new or modified information:
                        - Update only the relevant sections.
                        - Maintain data integrity for unchanged fields.
                        - Ensure the final output remains valid JSON.

                        Your response must include:
                        1. A list of improvement suggestions with reasons.
                        2. The revised LinkedIn profile in structured JSON format.
                        3. Optional keyword suggestions for better search visibility.

                        LinkedIn Profile Input (JSON):
                        {json.dumps(state["resume_details"])}

                        """

        if len(state["messages"]) == 0:
            state["messages"].append(SystemMessage(content=chatBotTemp))


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
