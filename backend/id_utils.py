from datetime import datetime
import uuid


def generate_benchmark_id():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    short_id = str(uuid.uuid4())[:8]

    return f"BMK-{timestamp}-{short_id}"


def generate_request_id():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    short_id = str(uuid.uuid4())[:8]

    return f"REQ-{timestamp}-{short_id}"


def current_timestamp():
    return datetime.now().isoformat()