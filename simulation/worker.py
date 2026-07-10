import time
from .models import SimulationConfig
from .simulator import generate_data
from api.models import SensorData

def start_simulation():
    t = 0

    while True:
        config = SimulationConfig.objects.first()

        if config and config.is_running:

            data = generate_data(config, t)

            SensorData.objects.create(
                vibration=data["vibration"],
                temperature=data["temperature"],
                pressure=data["pressure"],
                torque=data["torque"]
            )

            t += 1

        time.sleep(config.interval if config else 2)