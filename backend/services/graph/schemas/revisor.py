from pydantic import BaseModel

class RevisorOutputSchema(BaseModel):
    next_agent: str
    query_web: str