def build_recommendation(fault_name, health_value, probability):
    if fault_name == "Bearing Wear" and (health_value < 70 or probability >= 60):
        action = "Arrêt planifié et remplacement des roulements"
        priority = "HIGH"
    elif fault_name == "Cooling Failure" and (health_value < 70 or probability >= 60):
        action = "Arrêt moteur et inspection du système de refroidissement"
        priority = "HIGH"
    elif fault_name == "Motor Overload" and (health_value < 75 or probability >= 60):
        action = "Réduire la charge et vérifier le procédé"
        priority = "HIGH"
    else:
        action = "Actions préventives et surveillance continue"
        if health_value < 50 or probability > 80:
            priority = "HIGH"
        elif health_value < 80 or probability >= 50:
            priority = "MEDIUM"
        else:
            priority = "LOW"

    if health_value < 40 or probability > 85:
        priority = "HIGH"
    elif priority != "HIGH" and (health_value < 70 or probability >= 70):
        priority = "MEDIUM"

    return {
        "action": action,
        "priority": priority,
    }

