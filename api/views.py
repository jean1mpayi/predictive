from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response

from .models import SensorData
from .serializers import SensorDataSerializer

from .services.maintenance import analyze_sensor_data, maintenance_engine
from simulation.models import SimulationConfig
from simulation.services.runtime import get_engine



class SensorDataViewSet(viewsets.ModelViewSet):

    queryset = SensorData.objects.all()

    serializer_class = SensorDataSerializer



    def create(self, request, *args, **kwargs):


        # ----------------------------
        # Données reçues
        # ----------------------------

        data = request.data.copy()



        # ----------------------------
        # Analyse maintenance
        # ----------------------------

        analysis = analyze_sensor_data(
            data
        )

        data["health"] = analysis["health"]



        # ----------------------------
        # Sauvegarde historique capteur
        # ----------------------------

        save_data = {
            "temperature": data.get("temperature", 0),
            "vibration": data.get("vibration", 0),
            "current": data.get("current", 0),
            "torque": data.get("torque", 0),
            "speed": data.get("speed", 0),
            "health": data["health"],
        }

        serializer = self.get_serializer(data=save_data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()



        # ----------------------------
        # Réponse complète
        # ----------------------------

        return Response(

            {

                "sensor": save_data,

                "maintenance": analysis

            }

        )


def latest_sensor(request):
    """
    Return the dashboard-ready payload for the latest machine state.
    """

    latest = SensorData.objects.order_by("-timestamp").first()
    recent_measurements = SensorData.objects.order_by("-timestamp")[:12]
    simulation_config = SimulationConfig.objects.first()
    simulation_engine = get_engine()

    if latest is None:
        sensor_data = {
            "temperature": round(float(simulation_engine.motor.internal_temperature), 2),
            "vibration": round(float(simulation_engine.motor.vibration), 3),
            "current": round(float(simulation_engine.motor.current), 2),
            "torque": round(float(simulation_engine.motor.torque), 2),
            "speed": round(float(simulation_engine.motor.speed), 2),
            "load": round(float(simulation_engine.motor.load), 2),
            "wear": round(float(simulation_engine.motor.wear), 2),
            "misalignment": round(float(simulation_engine.motor.misalignment), 2),
            "runtime": round(float(simulation_engine.motor.runtime), 2),
        }
    else:
        latest_data = SensorDataSerializer(latest).data
        sensor_data = {
            "temperature": latest_data.get("temperature", 0.0),
            "vibration": latest_data.get("vibration", 0.0),
            "current": latest_data.get("current", 0.0),
            "torque": latest_data.get("torque", 0.0),
            "speed": latest_data.get("speed", 0.0),
            "load": simulation_engine.motor.load,
            "wear": simulation_engine.motor.wear,
            "misalignment": simulation_engine.motor.misalignment,
            "runtime": simulation_engine.motor.runtime,
        }

    analyze_sensor_data(sensor_data)
    payload = maintenance_engine.build_payload(
        motor=simulation_engine.motor,
        simulation={
            "running": bool(simulation_config.is_running) if simulation_config else simulation_engine.running,
            "mode": "SIMULATION",
            "fault": simulation_config.fault_mode if simulation_config else simulation_engine.fault_injector.current_fault,
        },
        sensor_data=sensor_data,
    )

    history = []
    for item in reversed(recent_measurements):
        item_data = SensorDataSerializer(item).data
        history.append(
            {
                "timestamp": item_data.get("timestamp"),
                "temperature": item_data.get("temperature", 0.0),
                "vibration": item_data.get("vibration", 0.0),
                "current": item_data.get("current", 0.0),
                "torque": item_data.get("torque", 0.0),
                "speed": item_data.get("speed", 0.0),
                "health": item_data.get("health", 0.0),
            }
        )

    payload["history"] = history

    return JsonResponse(payload)
