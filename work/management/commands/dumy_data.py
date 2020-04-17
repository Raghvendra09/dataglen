from django.core.management.base import BaseCommand, CommandError
import datetime
import random
from work.models import SensorData

class Command(BaseCommand):
    help = 'Command to do........'

    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        sensor_type = ['Temprature', 'Proximity', 'Accelerometer', 'Pressure', 'Light']
        for i in range(0, 250):
         timestamp = (datetime.datetime.now()- datetime.timedelta(days=250)) + datetime.timedelta(days=i)
         reading = random.randint(40,100)
         index  = random.randint(0,4)
         sensor_name = sensor_type[index]
         SensorData.objects.create(reading=reading, timestamp=timestamp, sensor_type=sensor_name)


