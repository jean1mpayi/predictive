def build_alert(health_value, probability):
    if probability > 80 or health_value < 50:
        return {
            "status": "CRITICAL",
            "color": "red",
            "icon": "🚨",
            "priority": "HIGH",
            "message": "Immediate maintenance required",
        }

    if health_value < 80:
        return {
            "status": "WARNING",
            "color": "orange",
            "icon": "⚠️",
            "priority": "MEDIUM",
            "message": "Degradation detected, monitor the asset",
        }

    return {
        "status": "NORMAL",
        "color": "green",
        "icon": "✅",
        "priority": "LOW",
        "message": "Asset operating normally",
    }

