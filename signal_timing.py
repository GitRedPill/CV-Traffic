def estimate_density(vehicle_counts):
    """
    Estimate traffic density based on average vehicle count.
    Returns density level and average count.
    """
    if not vehicle_counts:
        return "No Data", 0

    avg_count = sum(vehicle_counts) / len(vehicle_counts)

    if avg_count < 5:
        density = "Low"
    elif avg_count < 15:
        density = "Medium"
    else:
        density = "High"

    return density, avg_count

def compute_signal_time(density):
    """
    Compute recommended green signal time based on density.
    Rule-based: Low=30s, Medium=45s, High=60s.
    """
    timing = {
        "Low": 30,
        "Medium": 45,
        "High": 60,
        "No Data": 30
    }
    return timing.get(density, 30)