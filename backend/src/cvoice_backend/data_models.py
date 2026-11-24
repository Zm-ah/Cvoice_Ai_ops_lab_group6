"""Pydantic models shared by the API and the agents."""

from pydantic import BaseModel, Field


class Job(BaseModel):
    title: str = Field(description="job title, for example 'Data Engineer'")
    company: str = Field(description="name of the company")
    start_year: int | None = Field(description="year the job started, None if unknown")
    end_year: int | None = Field(description="year the job ended, None if it is the current job")
    description: str = Field(description="one or two sentences about what the person did")


class Profile(BaseModel):
    name: str = Field(description="full name of the person")
    headline: str = Field(description="current or most recent role, in a few words")
    years_of_experience: int = Field(description="total years of work experience, rounded")
    skills: list[str] = Field(description="the most important skills, at most 10")
    jobs: list[Job] = Field(description="all jobs, the most recent first")
    summary: str = Field(description="short summary of the person, at most 4 sentences")


class MatchResult(BaseModel):
    score: int = Field(ge=0, le=100, description="how well the profile matches the job ad, 0 to 100")
    matching_skills: list[str] = Field(description="skills in the job ad that the person has")
    missing_skills: list[str] = Field(description="skills in the job ad that the person lacks")
    motivation: str = Field(description="short explanation of the score, at most 3 sentences")
