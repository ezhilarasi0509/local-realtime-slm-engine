from fastapi import APIRouter
from pydantic import BaseModel

from ollama_client import generate_response
from experiment_utils import (
    calculate_consistency,
    calculate_variance
)

router = APIRouter()


class TemperatureExperimentRequest(BaseModel):
    model: str
    prompt: str
    runs: int = 3


@router.post("/temperature-experiment")
def temperature_experiment(
    req: TemperatureExperimentRequest
):

    temperatures = [0, 0.7]

    experiment_results = []

    for temp in temperatures:

        responses = []
        latencies = []
        ttfts = []

        for _ in range(req.runs):

            result = generate_response(
                model=req.model,
                prompt=req.prompt,
                temperature=temp
            )

            response_text = str(
                result["response"]
            )

            responses.append(response_text)

            latencies.append(
                result["inference_time"]
            )

            ttfts.append(
                result["ttft"]
            )

        avg_latency = round(
            sum(latencies) / len(latencies),
            2
        )

        avg_ttft = round(
            sum(ttfts) / len(ttfts),
            2
        )

        consistency_score = calculate_consistency(
            responses
        )

        variance_score = calculate_variance(
            responses
        )

        experiment_results.append({
            "temperature": temp,
            "runs": req.runs,
            "avg_latency": avg_latency,
            "avg_ttft": avg_ttft,
            "consistency_score": consistency_score,
            "variance_score": variance_score,
            "responses": responses
        })

    return {
        "model": req.model,
        "prompt": req.prompt,
        "experiment": experiment_results
    }