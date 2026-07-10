from django.db import models

class SimulationConfig(models.Model):
    is_running = models.BooleanField(default=False)
    mode_auto = models.BooleanField(default=True)
    interval = models.IntegerField(default=2)  # secondes

    # type de panne injectée
    fault_mode = models.CharField(
        max_length=50,
        default="normal"
    )

    def __str__(self):
        return f"Simulation ({'ON' if self.is_running else 'OFF'})"