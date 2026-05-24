from pydantic import BaseModel
from typing import List


class StructuredLLMResponse(BaseModel):
    topic: str
    definition: str
    key_points: List[str]
    example: str