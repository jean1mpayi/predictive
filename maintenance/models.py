from django.db import models

class Alert(models.Model):
    URGENCY_CHOICES = [
        ('INFO', 'INFO'),
        ('WARNING', 'WARNING'),
        ('ERROR', 'ERROR'),
        ('CRITICAL', 'CRITICAL')
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    fault_type = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.urgency}] {self.title} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
