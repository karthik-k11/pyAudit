def calculate_health_score(
    missing_count=0,
    mismatch_count=0,
    import_failure_count=0,
    invalid_requirement_count=0,
):
    score = 100

    score -= missing_count * 20
    score -= mismatch_count * 15
    score -= import_failure_count * 20
    score -= invalid_requirement_count * 10

    score = max(score, 0)

    if score >= 100:
        status = "Healthy"
    elif score >= 80:
        status = "Good"
    elif score >= 60:
        status = "Needs Attention"
    else:
        status = "Unhealthy"

    return {
        "score": score,
        "status": status,
    }