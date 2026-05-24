from typing import List


# ==========================================
# CONSISTENCY SCORE
# ==========================================
def calculate_consistency(
    responses: List[str]
):

    if len(responses) <= 1:
        return 10

    lengths = [
        len(r.split())
        for r in responses
    ]

    average = (
        sum(lengths)
        / len(lengths)
    )

    variance = sum(
        abs(
            x - average
        )
        for x in lengths
    ) / len(lengths)

    score = max(
        1,
        10 - (variance / 5)
    )

    return round(score,2)


# ==========================================
# VARIANCE SCORE
# ==========================================
def calculate_variance(
    responses: List[str]
):

    lengths = [
        len(r.split())
        for r in responses
    ]

    avg = (
        sum(lengths)
        / len(lengths)
    )

    variance = sum(
        (
            x-avg
        )**2
        for x in lengths
    ) / len(lengths)

    return round(
        variance,
        2
    )