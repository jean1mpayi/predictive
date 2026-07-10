from django.http import JsonResponse

from .faults import FAULT_SCENARIOS
from .services.runtime import get_engine, start_engine, stop_engine, set_fault_mode
from .models import SimulationConfig

def start_simulation(request):
    config = SimulationConfig.objects.first()

    if config is None:
        config = SimulationConfig.objects.create()

    config.is_running = True
    config.save()

    start_engine()

    return JsonResponse({"status": "simulation started"})


def stop_simulation(request):
    config = SimulationConfig.objects.first()

    if config is None:
        config = SimulationConfig.objects.create()

    config.is_running = False
    config.save()

    stop_engine()

    return JsonResponse({"status": "simulation stopped"})


def set_fault(request, name):
    """Select the active fault scenario from the dashboard."""

    normalized_name = name.upper()

    if normalized_name not in FAULT_SCENARIOS:
        return JsonResponse(
            {
                "status": "error",
                "message": f"Unknown fault scenario: {name}",
            },
            status=400,
        )

    selected_fault = set_fault_mode(normalized_name)
    engine = get_engine()

    return JsonResponse(
        {
            "status": "fault updated",
            "fault_mode": selected_fault,
            "motor": {
                "running": getattr(getattr(engine, "motor", None), "running", None),
                "load": getattr(getattr(engine, "motor", None), "load", None),
                "wear": getattr(getattr(engine, "motor", None), "wear", None),
                "misalignment": getattr(getattr(engine, "motor", None), "misalignment", None),
                "cooling_efficiency": getattr(getattr(engine, "motor", None), "cooling_efficiency", None),
            },
        }
    )
