from django.db import models

# Create your models here.

class SensorData(models.Model):
    reading = models.FloatField(blank=True, null=True)
    received_at = models.DateTimeField(auto_now_add=True)
    sensor_type = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'production_data'
