from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from ollama_client import generate_response

from benchmark_utils import (
    calculate_speed_score,
    calculate_quality_score,
    calculate_relevance_score,
    calculate_completeness_score,
    calculate_structure_score,
    calculate_final_score,
)

router = APIRouter()


class QuantizationExperimentRequest(BaseModel):
    prompt: str
    models: List[str] = ["llama3", "mistral", "phi3"]
    temperature: float = 0.0


@router.post("/quantization")
def quantization_experiment(req: QuantizationExperimentRequest):
    results = []

    for model in req.models:
        result = generate_response(
            model=model,
            prompt=req.prompt,
            temperature=req.temperature
        )

        response = result["response"]

        definition = response.get("definition", "")
        key_points = response.get("key_points", [])

        token_count = (
            len(definition.split())
            + sum(len(point.split()) for point in key_points)
        )

        inference_time = result["inference_time"]
        latency_ms = round(inference_time * 1000, 2)

        tokens_per_sec = round(
            token_count / max(inference_time, 1),
            2
        )

        speed_score = calculate_speed_score(latency_ms)
        quality_score = calculate_quality_score(token_count)
        relevance_score = calculate_relevance_score(req.prompt, definition)
        completeness_score = calculate_completeness_score(token_count)
        structure_score = calculate_structure_score(response)

        final_score = calculate_final_score(
            speed_score,
            quality_score,
            relevance_score,
            completeness_score,
            structure_score
        )

        results.append({
            "model": model,
            "valid_output": result["valid_output"],
            "retry_count": result["retry_count"],
            "latency_ms": latency_ms,
            "time_to_first_token": result["ttft"],
            "inference_time": inference_time,
            "tokens_per_sec": tokens_per_sec,
            "token_count": token_count,
            "quality_score": quality_score,
            "speed_score": speed_score,
            "relevance_score": relevance_score,
            "completeness_score": completeness_score,
            "structure_score": structure_score,
            "final_score": final_score,
            "response": response
        })

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return {
        "experiment": "model_quality_speed_tradeoff",
        "note": "Use this endpoint to compare normal and quantized model tags when installed, for example llama3, llama3:q4, llama3:q5.",
        "prompt": req.prompt,
        "temperature": req.temperature,
        "best_model": results[0]["model"],
        "results": results
    }