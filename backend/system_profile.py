import platform
import sys
import psutil
import subprocess


def get_installed_ollama_models():
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return []

        lines = result.stdout.strip().split("\n")

        models = []

        for line in lines[1:]:
            parts = line.split()

            if len(parts) >= 3:
                models.append({
                    "name": parts[0],
                    "id": parts[1],
                    "size": parts[2]
                })

        return models

    except Exception:
        return []


def get_system_profile():
    memory = psutil.virtual_memory()

    return {
        "machine": {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version.split()[0]
        },

        "hardware": {
            "cpu_cores_physical": psutil.cpu_count(logical=False),
            "cpu_cores_logical": psutil.cpu_count(logical=True),
            "total_ram_gb": round(memory.total / (1024 ** 3), 2),
            "available_ram_gb": round(memory.available / (1024 ** 3), 2),
            "ram_usage_percent": memory.percent
        },

        "ollama": {
            "installed_models": get_installed_ollama_models()
        },

        "benchmark_environment": {
            "execution_mode": "local_offline",
            "network_dependency": "none_for_inference",
            "privacy": "prompts_and_outputs_remain_on_local_machine",
            "cost_model": "no_external_api_cost",
            "deployment_context": "edge_or_local_device"
        }
    }