from predictive.health import HealthCalculator
from predictive.faults import FaultDetector
from predictive.recommendations import RecommendationEngine
from predictive.rul import RULCalculator
from predictive.alerts import AlertManager


class PredictiveAnalyzer:
    """
    Analyseur principal de maintenance prédictive.

    Ce module centralise toutes les analyses :

        - Calcul de l'indice de santé
        - Détection des défauts
        - Niveau d'alerte
        - Estimation de la durée de vie restante (RUL)
        - Recommandation de maintenance
    """

    def __init__(self):

        self.health = HealthCalculator()

        self.faults = FaultDetector()

        self.rul = RULCalculator()

        self.recommendation = RecommendationEngine()

        self.alert = AlertManager()

    # =======================================================
    # Analyse complète
    # =======================================================

    def analyze(self, sensor_data: dict):

        # ------------------------------
        # 1. Calcul de l'état de santé
        # ------------------------------

        health = self.health.compute(sensor_data)

        # ------------------------------
        # 2. Détection des défauts
        # ------------------------------

        fault = self.faults.detect(sensor_data)

        # ------------------------------
        # 3. Niveau d'alerte
        # ------------------------------

        alert = self.alert.evaluate(
            health,
            fault
        )

        # ------------------------------
        # 4. Estimation RUL
        # ------------------------------

        rul = self.rul.compute(
            sensor_data,
            health
        )

        # ------------------------------
        # 5. Recommandation
        # ------------------------------

        recommendation = self.recommendation.generate(
            fault,
            health,
            rul
        )

        # ------------------------------
        # Résultat final
        # ------------------------------

        return {

            "health": health,

            "status": alert["status"],

            "alert": alert["level"],

            "color": alert["color"],

            "fault": fault["fault"],

            "probability": fault["probability"],

            "recommendation": recommendation,

            "rul": rul

        }