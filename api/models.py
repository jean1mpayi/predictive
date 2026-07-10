from django.db import models


class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    temperature = models.FloatField()
    vibration = models.FloatField()
    current = models.FloatField()
    torque = models.FloatField()
    speed = models.FloatField()

    health = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}"