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
    score: int = Field(
        ge=0, le=100, description="how well the profile matches the job ad, 0 to 100"
    )
    matching_skills: list[str] = Field(description="skills in the job ad that the person has")
    missing_skills: list[str] = Field(description="skills in the job ad that the person lacks")
    motivation: str = Field(description="short explanation of the score, at most 3 sentences")


class Chunk(BaseModel):
    """A piece of a document, tagged with the profile it belongs to."""

    chunk_id: str = Field(description="unique id of this chunk")
    profile_id: str = Field(description="the profile the chunk belongs to")
    text: str = Field(description="the text of the chunk")
    source: str = Field(description="file name the chunk was read from")
    position: int = Field(description="position of the chunk in its document, starting at 0")


class UploadResponse(BaseModel):
    """What the upload endpoint returns once the documents are indexed."""

    profile_id: str = Field(description="id to use when asking about this person")
    sources: list[str] = Field(description="file names that were read")
    chunk_count: int = Field(description="number of chunks stored for this profile")
    characters: int = Field(description="how much text was extracted in total")