from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from schemas import ChatRequest, BenchmarkResponse

from benchmark_utils import (
    calculate_speed_score,
    calculate_quality_score,
    calculate_relevance_score,
    calculate_completeness_score,
    calculate_structure_score,
    calculate_final_score,
)

from ollama_client import generate_response

from experiment_routes import router as experiment_router
from quantization_routes import router as quantization_router

from report_utils import (
    save_benchmark_run,
    export_history_json,
    export_history_csv,
)

from suite_report_utils import (
    save_suite_run,
    export_suite_history_json,
)

from final_report_utils import generate_final_summary_report

from benchmark_suite import BENCHMARK_PROMPTS
from system_profile import get_system_profile

from id_utils import (
    generate_benchmark_id,
    generate_request_id,
    current_timestamp,
)


app = FastAPI(
    title="Local LLM Benchmark API",
    version="10.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    experiment_router,
    prefix="/api/v1/experiments",
    tags=["Experiments"]
)


app.include_router(
    quantization_router,
    prefix="/api/v1/experiments",
    tags=["Experiments"]
)


MODEL_METADATA = {
    "llama3": {"size": 4.7},
    "mistral": {"size": 4.1},
    "phi3": {"size": 2.3},
}


@app.get("/")
def health():
    return {
        "status": "healthy",
        "service": "Local LLM Benchmark API",
        "version": "10.0.0"
    }


@app.get("/api/v1/system/profile")
def system_profile():
    return get_system_profile()


@app.post("/chat")
def chat(req: ChatRequest):
    request_id = generate_request_id()

    result = generate_response(
        model=req.model,
        prompt=req.prompt,
        temperature=req.temperature
    )

    return {
        "request_id": request_id,
        "timestamp": current_timestamp(),
        "model": req.model,
        "response": result["response"],
        "latency_ms": round(result["inference_time"] * 1000, 2),
        "time_to_first_token": result["ttft"],
        "inference_time": result["inference_time"],
        "valid_output": result["valid_output"],
        "retry_count": result["retry_count"]
    }


@app.post("/benchmark", response_model=BenchmarkResponse)
def benchmark(req: ChatRequest):
    benchmark_id = generate_benchmark_id()
    request_id = generate_request_id()
    timestamp = current_timestamp()

    models = ["llama3", "mistral", "phi3"]
    results = []

    for model in models:
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

        reliability_score = 10 if result["valid_output"] else 2

        final_score = calculate_final_score(
            speed_score,
            quality_score,
            relevance_score,
            completeness_score,
            structure_score
        )

        final_score = round(
            (final_score * 0.90) + (reliability_score * 0.10),
            2
        )

        results.append({
            "model": model,
            "response": response,
            "model_size": MODEL_METADATA[model]["size"],
            "ram_usage": MODEL_METADATA[model]["size"],
            "tokens_per_sec": tokens_per_sec,
            "token_count": token_count,
            "inference_time": inference_time,
            "response_length": len(str(response)),
            "latency_ms": latency_ms,
            "time_to_first_token": result["ttft"],
            "speed_score": speed_score,
            "quality_score": quality_score,
            "relevance_score": relevance_score,
            "completeness_score": completeness_score,
            "structure_score": structure_score,
            "final_score": final_score,
            "valid_output": result["valid_output"],
            "retry_count": result["retry_count"]
        })

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    leaderboard = [
        {
            "rank": index,
            "model": item["model"],
            "score": item["final_score"]
        }
        for index, item in enumerate(results, start=1)
    ]

    best_model = results[0]

    why_model_won = []

    if best_model["quality_score"] >= 8:
        why_model_won.append("Higher response quality")

    if best_model["structure_score"] >= 8:
        why_model_won.append("Well structured output")

    if best_model["valid_output"]:
        why_model_won.append("Reliable JSON output")

    if best_model["retry_count"] == 0:
        why_model_won.append("No retry needed")

    response_data = {
        "benchmark_id": benchmark_id,
        "request_id": request_id,
        "timestamp": timestamp,
        "prompt": req.prompt,
        "best_model": best_model["model"],
        "why_model_won": why_model_won,
        "leaderboard": leaderboard,
        "results": results
    }

    save_benchmark_run(response_data)

    return response_data


@app.get("/api/v1/reports/history")
def history():
    return {
        "history": export_history_json()
    }


@app.get("/api/v1/reports/export-json")
def export_json():
    return {
        "history": export_history_json()
    }


@app.get("/api/v1/reports/export-csv")
def export_csv():
    csv_file = export_history_csv()

    return FileResponse(
        csv_file,
        media_type="text/csv",
        filename="benchmark_report.csv"
    )


@app.get("/api/v1/reports/final-summary")
def final_summary_report():
    return generate_final_summary_report()


def run_suite(prompts):
    suite_results = []
    model_totals = {}

    for item in prompts:
        req = ChatRequest(
            model="llama3",
            prompt=item["prompt"],
            temperature=0
        )

        result = benchmark(req)

        suite_results.append({
            "category": item["category"],
            "prompt": item["prompt"],
            "best_model": result["best_model"],
            "leaderboard": result["leaderboard"]
        })

        for entry in result["leaderboard"]:
            model = entry["model"]
            score = entry["score"]

            if model not in model_totals:
                model_totals[model] = {
                    "total_score": 0,
                    "runs": 0,
                    "wins": 0
                }

            model_totals[model]["total_score"] += score
            model_totals[model]["runs"] += 1

            if entry["rank"] == 1:
                model_totals[model]["wins"] += 1

    average_scores = []

    for model, data in model_totals.items():
        average_scores.append({
            "model": model,
            "average_score": round(
                data["total_score"] / data["runs"],
                2
            ),
            "wins": data["wins"],
            "runs": data["runs"]
        })

    average_scores.sort(
        key=lambda x: x["average_score"],
        reverse=True
    )

    response_data = {
        "total_prompts": len(prompts),
        "overall_best_model": average_scores[0]["model"],
        "average_scores": average_scores,
        "suite_results": suite_results
    }

    save_suite_run(response_data)

    return response_data


@app.post("/api/v1/benchmark-suite/run-small")
def run_small_benchmark_suite():
    small_prompts = BENCHMARK_PROMPTS[:5]

    return run_suite(small_prompts)


@app.post("/api/v1/benchmark-suite/run")
def run_full_benchmark_suite():
    return run_suite(BENCHMARK_PROMPTS)


@app.get("/api/v1/benchmark-suite/history")
def benchmark_suite_history():
    return {
        "history": export_suite_history_json()
    }


@app.get("/api/v1/benchmark-suite/export-json")
def benchmark_suite_export_json():
    return {
        "history": export_suite_history_json()
    }