from typing import Optional, List
from llama_index.core.tools.function_tool import FunctionTool
from pydantic import BaseModel, Field


class CreateResumeToolParams(BaseModel):
    candidate_name: str = Field(
        description="The full name of the candidate whose resume is being created."
    )
    email: str = Field(description="The contact email of the candidate.")
    phone: Optional[str] = Field(
        description="The candidate's contact phone number.", default=None
    )
    summary: Optional[str] = Field(
        description="A short professional summary of the candidate.", default=None
    )
    skills: Optional[List[str]] = Field(
        description="A list of skills the candidate possesses.", default=None
    )
    experience: Optional[List[str]] = Field(
        description="A list of previous job experiences in chronological order.",
        default=None,
    )
    education: Optional[List[str]] = Field(
        description="A list of educational qualifications the candidate has obtained.",
        default=None,
    )


def create_resume(
    candidate_name: str,
    email: str,
    phone: Optional[str] = None,
    summary: Optional[str] = None,
    skills: Optional[List[str]] = None,
    experience: Optional[List[str]] = None,
    education: Optional[List[str]] = None,
):
    """Formats the given candidate information into a structured Markdown resume."""

    resume_template = f"""\
# {candidate_name}

📧 **Email:** {email}  
📞 **Phone:** {phone if phone else 'N/A'}

---

## 🔹 Summary  
{summary if summary else 'N/A'}

---

## 🔹 Skills  
{', '.join(skills) if skills else 'N/A'}

---

## 🔹 Experience  
{chr(10).join(f"- {exp}" for exp in experience) if experience else 'N/A'}

---

## 🔹 Education  
{chr(10).join(f"- {edu}" for edu in education) if education else 'N/A'}

---
"""

    return {"resume": resume_template}


def create_create_resume_tool():
    """Creates and returns the resume generation tool for the bot."""
    create_resume_tool = FunctionTool.from_defaults(
        name="create_resume_tool",
        description="Formats a structured resume from candidate information using Markdown.",
        fn_schema=CreateResumeToolParams,
        fn=create_resume,
    )
    return create_resume_tool
