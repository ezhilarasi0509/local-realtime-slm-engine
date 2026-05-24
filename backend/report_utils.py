import json
import csv
import os
from datetime import datetime

HISTORY_FILE = "benchmark_history.json"
CSV_FILE = "benchmark_report.csv"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return []


def save_benchmark_run(data):
    history = load_history()

    record = {
        "benchmark_id": data.get("benchmark_id"),
        "request_id": data.get("request_id"),
        "timestamp": data.get("timestamp", datetime.now().isoformat()),
        "prompt": data["prompt"],
        "best_model": data["best_model"],
        "leaderboard": data["leaderboard"],
        "results": data["results"],
        "why_model_won": data["why_model_won"],
    }

    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

    return record


def export_history_json():
    return load_history()


def export_history_csv():
    history = load_history()

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "benchmark_id",
            "request_id",
            "timestamp",
            "prompt",
            "best_model",
            "model",
            "final_score",
            "latency_ms",
            "time_to_first_token",
            "tokens_per_sec",
            "valid_output",
            "retry_count",
        ])

        for run in history:
            for result in run["results"]:
                writer.writerow([
                    run.get("benchmark_id"),
                    run.get("request_id"),
                    run.get("timestamp"),
                    run.get("prompt"),
                    run.get("best_model"),
                    result.get("model"),
                    result.get("final_score"),
                    result.get("latency_ms"),
                    result.get("time_to_first_token"),
                    result.get("tokens_per_sec"),
                    result.get("valid_output"),
                    result.get("retry_count"),
                ])

    return CSV_FILE