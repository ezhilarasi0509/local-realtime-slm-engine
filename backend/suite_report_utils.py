import json
import os
from datetime import datetime


SUITE_HISTORY_FILE = "benchmark_suite_history.json"


def load_suite_history():
    if not os.path.exists(SUITE_HISTORY_FILE):
        return []

    try:
        with open(SUITE_HISTORY_FILE, "r") as file:
            return json.load(file)

    except Exception:
        return []


def save_suite_run(data):
    history = load_suite_history()

    record = {
        "timestamp": datetime.now().isoformat(),
        "total_prompts": data["total_prompts"],
        "overall_best_model": data["overall_best_model"],
        "average_scores": data["average_scores"],
        "suite_results": data["suite_results"]
    }

    history.append(record)

    with open(SUITE_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

    return record


def export_suite_history_json():
    return load_suite_history()