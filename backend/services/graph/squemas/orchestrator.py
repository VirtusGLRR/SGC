from pydantic import BaseModel

class OrquestrationOutputSchema(BaseModel):
    next_agent: str
    orquestration_explaination: str