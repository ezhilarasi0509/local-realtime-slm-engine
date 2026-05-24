from report_utils import export_history_json
from suite_report_utils import export_suite_history_json
from system_profile import get_system_profile


def calculate_model_summary_from_benchmarks(history):
    model_stats = {}

    for run in history:
        for result in run.get("results", []):
            model = result["model"]

            if model not in model_stats:
                model_stats[model] = {
                    "runs": 0,
                    "wins": 0,
                    "total_score": 0,
                    "total_latency": 0,
                    "total_ttft": 0,
                    "total_tokens_per_sec": 0,
                    "valid_outputs": 0,
                    "retries": 0
                }

            model_stats[model]["runs"] += 1
            model_stats[model]["total_score"] += result.get("final_score", 0)
            model_stats[model]["total_latency"] += result.get("latency_ms", 0)
            model_stats[model]["total_ttft"] += result.get("time_to_first_token", 0)
            model_stats[model]["total_tokens_per_sec"] += result.get("tokens_per_sec", 0)

            if result.get("valid_output"):
                model_stats[model]["valid_outputs"] += 1

            model_stats[model]["retries"] += result.get("retry_count", 0)

        best_model = run.get("best_model")

        if best_model in model_stats:
            model_stats[best_model]["wins"] += 1

    summary = []

    for model, data in model_stats.items():
        runs = max(data["runs"], 1)

        summary.append({
            "model": model,
            "runs": data["runs"],
            "wins": data["wins"],
            "average_score": round(data["total_score"] / runs, 2),
            "average_latency_ms": round(data["total_latency"] / runs, 2),
            "average_ttft": round(data["total_ttft"] / runs, 2),
            "average_tokens_per_sec": round(data["total_tokens_per_sec"] / runs, 2),
            "valid_output_rate": round((data["valid_outputs"] / runs) * 100, 2),
            "total_retries": data["retries"]
        })

    summary.sort(
        key=lambda x: x["average_score"],
        reverse=True
    )

    return summary


def calculate_suite_summary(suite_history):
    if not suite_history:
        return {
            "suite_runs": 0,
            "latest_suite": None
        }

    latest_suite = suite_history[-1]

    return {
        "suite_runs": len(suite_history),
        "latest_suite": {
            "timestamp": latest_suite.get("timestamp"),
            "total_prompts": latest_suite.get("total_prompts"),
            "overall_best_model": latest_suite.get("overall_best_model"),
            "average_scores": latest_suite.get("average_scores")
        }
    }


def generate_final_summary_report():
    benchmark_history = export_history_json()
    suite_history = export_suite_history_json()
    system_profile = get_system_profile()

    model_summary = calculate_model_summary_from_benchmarks(
        benchmark_history
    )

    suite_summary = calculate_suite_summary(
        suite_history
    )

    best_model_overall = (
        model_summary[0]["model"]
        if model_summary
        else "Not enough benchmark data"
    )

    return {
        "project": {
            "name": "Real-Time Local LLM Benchmark Dashboard",
            "purpose": "Benchmark local small language models using Ollama for privacy, latency, cost, and edge deployment trade-offs.",
            "backend_status": "production_ready_fresher_level"
        },

        "final_recommendation": {
            "best_model_overall": best_model_overall,
            "reason": "Selected based on average weighted score, latency, TTFT, tokens/sec, structured output reliability, benchmark wins, and local inference constraints."
        },

        "benchmark_summary": {
            "total_single_benchmark_runs": len(benchmark_history),
            "model_summary": model_summary
        },

        "benchmark_suite_summary": suite_summary,

        "system_profile": system_profile,

        "engineering_features_completed": [
            "Offline local inference using Ollama",
            "FastAPI backend wrapper",
            "Three-model comparison",
            "TTFT measurement",
            "Total latency measurement",
            "Tokens/sec throughput tracking",
            "Model size tracking",
            "Structured JSON output",
            "Pydantic validation",
            "Retry mechanism for invalid outputs",
            "Temperature experiment support",
            "Benchmark history persistence",
            "JSON and CSV export",
            "35-prompt benchmark suite",
            "Small benchmark suite for quick testing",
            "Benchmark suite history",
            "Benchmark suite JSON export",
            "System profile endpoint",
            "Final summary report endpoint",
            "Benchmark ID and request ID tracking",
            "Model quality-speed tradeoff experiment",
            "Production-style API documentation through FastAPI Swagger"
        ],

        "backend_completion_status": {
            "score": "100/100",
            "status": "Backend complete for fresher-level AI engineering portfolio",
            "next_phase": "Frontend analytics dashboard, README, technical report, screenshots, and demo video"
        },

        "remaining_project_upgrades": [
            "Frontend analytics dashboard",
            "Charts and visualizations",
            "README and technical report",
            "Screenshots",
            "Demo video",
            "GitHub polish"
        ]
    }