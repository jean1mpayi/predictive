from predictive.engine import MaintenanceEngine


# Instance globale
# Le moteur garde son historique
# entre les appels API

maintenance_engine = MaintenanceEngine()



def analyze_sensor_data(data):

    """
    Envoie les données capteurs
    vers le moteur prédictif.
    """

    result = maintenance_engine.analyze(
        data
    )

    return result