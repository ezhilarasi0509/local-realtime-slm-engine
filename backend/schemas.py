from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    model: str
    prompt: str
    temperature: float = 0.0


class StructuredResponse(BaseModel):
    topic: str = Field(...)
    definition: str = Field(...)
    key_points: List[str] = Field(default_factory=list)
    example: str = Field(...)


class BenchmarkResult(BaseModel):
    model: str

    response: Dict[str, Any]

    model_size: float

    ram_usage: float

    tokens_per_sec: float

    token_count: int

    inference_time: float

    response_length: int

    latency_ms: float

    time_to_first_token: float

    speed_score: float

    quality_score: float

    relevance_score: float

    completeness_score: float

    structure_score: float

    final_score: float

    valid_output: bool

    retry_count: int


class LeaderboardEntry(BaseModel):
    rank: int
    model: str
    score: float


class BenchmarkResponse(BaseModel):
    benchmark_id: Optional[str] = None

    request_id: Optional[str] = None

    timestamp: Optional[str] = None

    prompt: str

    best_model: str

    why_model_won: List[str]

    leaderboard: List[LeaderboardEntry]

    results: List[BenchmarkResult]