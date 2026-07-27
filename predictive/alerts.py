def build_alert(health_value, probability):
    if probability > 80 or health_value < 50:
        return {
            "status": "CRITIQUE",
            "color": "red",
            "icon": "🚨",
            "priority": "ÉLEVÉ",
            "message": "Maintenance immédiate requise",
        }

    if health_value < 80:
        return {
            "status": "ATTENTION",
            "color": "orange",
            "icon": "⚠️",
            "priority": "MOYEN",
            "message": "Dégradation détectée, surveiller l’équipement",
        }

    return {
        "status": "NORMAL",
        "color": "green",
        "icon": "✅",
        "priority": "FAIBLE",
        "message": "L’équipement fonctionne normalement",
    }

