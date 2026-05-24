import re


# ==========================================
# TOKEN COUNT
# ==========================================
def get_token_count(text: str) -> int:
    return len(text.split())


# ==========================================
# TOKENS / SEC
# ==========================================
def calculate_tokens_per_sec(
    token_count: int,
    inference_time: float
) -> float:

    return round(
        token_count /
        max(inference_time, 1),
        2
    )


# ==========================================
# SPEED SCORE
# ==========================================
def calculate_speed_score(
    latency_ms: float
) -> float:

    score = 10 - (latency_ms / 5000)

    return round(
        max(1, min(score, 10)),
        2
    )


# ==========================================
# QUALITY SCORE
# ==========================================
def calculate_quality_score(
    token_count: int
) -> float:

    if token_count > 400:
        return 9.5
    elif token_count > 250:
        return 9.0
    elif token_count > 150:
        return 8.0
    elif token_count > 80:
        return 7.0

    return 5.0


# ==========================================
# RELEVANCE SCORE
# ==========================================
def calculate_relevance_score(
    prompt: str,
    response: str
) -> float:

    prompt_words = set(
        prompt.lower().split()
    )

    response_words = set(
        response.lower().split()
    )

    overlap = len(
        prompt_words.intersection(
            response_words
        )
    )

    score = overlap + 5

    return round(
        min(10, max(5, score)),
        2
    )


# ==========================================
# COMPLETENESS SCORE
# ==========================================
def calculate_completeness_score(
    token_count: int
) -> float:

    score = token_count / 40

    return round(
        min(10, max(5, score)),
        2
    )


# ==========================================
# STRUCTURE SCORE
# ==========================================
def calculate_structure_score(
    response: dict
) -> float:

    score = 7

    if response.get("topic"):
        score += 1

    if response.get("definition"):
        score += 1

    if response.get("key_points"):
        score += 0.5

    if response.get("example"):
        score += 0.5

    return round(
        min(score, 10),
        2
    )


# ==========================================
# FINAL SCORE
# ==========================================
def calculate_final_score(
    speed_score: float,
    quality_score: float,
    relevance_score: float,
    completeness_score: float,
    structure_score: float
) -> float:

    score = (
        quality_score * 0.35
        + speed_score * 0.20
        + relevance_score * 0.20
        + completeness_score * 0.15
        + structure_score * 0.10
    )

    return round(score, 2)