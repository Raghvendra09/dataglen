from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseForbidden
from django.views import View
from django.conf import settings
from jsonschema import validate
import jsonschema
import json
from .models import SensorData
import statistics
import time
import datetime
# Create your views here.

class MainApi(View):

    def get(self, request):
        sensor_type = request.GET.get('sensorType')
        start_date = request.GET.get("startDate")
        end_date = request.GET.get("endDate")
        table = request.GET.get("table")
        chart = request.GET.get("chart")
        all_sensor_types = request.GET.get("allSensorTypes")
        if table:
            sensor_data = SensorData.objects.defer()
            if start_date:
                sensor_data = sensor_data.filter(timestamp__date__gte=start_date)
            if end_date:
                sensor_data = sensor_data.filter(timestamp__date__lte=end_date)
            if sensor_type.lower() != "all":
                sensor_data = sensor_data.filter(sensor_type=sensor_type)
            sensor_data = list(sensor_data.values_list('reading', 'timestamp','sensor_type'))
            response = []
            for i in enumerate(sensor_data, 1):
                data = []
                data.append(i[0])
                data.append(i[1][2])
                data.append(i[1][0])
                data.append(i[1][1].strftime('%d-%h-%Y %I-%M %p'))
                response.append(data)
            return JsonResponse({"data": response}, safe=False)
        if chart:
            sensor_data = SensorData.objects.defer()
            if start_date:
                sensor_data = sensor_data.filter(timestamp__date__gte=start_date)
            if end_date:
                sensor_data = sensor_data.filter(timestamp__date__lte=end_date)
            if sensor_type.lower() != "all":
                sensor_data = sensor_data.filter(sensor_type=sensor_type)
            sensor_data = list(sensor_data.values_list('timestamp__date','reading'))
            response = [['Date', sensor_type]]
            reading_data = []
            for i in sensor_data:
                response.append([i[0], i[1]])
                reading_data.append(i[1])
            aggregated_data = {"max":max(reading_data),
                                "min": min(reading_data),
                                "mean": round(statistics.mean(reading_data),2)}
            return JsonResponse({"data": response, "aggregatedData": aggregated_data}, safe=False)
        if all_sensor_types:
            sensor_types = list(SensorData.objects.values_list('sensor_type', flat=True).distinct())
            return JsonResponse({"data":sensor_types}, safe=False)
        return render(request, 'dashboard.html')

    @staticmethod
    def validate_incoming_data():
        schema = {
            "type": "object",
            "properties": {
                "sensorType": {"type": "string"},
                "reading": {"type": "number", "pattern": "\d+\.{0,1}\d*"},
                "timestamp": {"type": "number"},
            },
            "required": ["sensorType", "reading", "timestamp"]
            }
        return schema

    def save_data(self, reading, timestamp, sensor_type):
        try:
            timestamp = datetime.datetime.utcfromtimestamp(timestamp)
            SensorData.objects.create(reading=reading, timestamp=timestamp, sensor_type=sensor_type)
            return
        except Exception as ex:
            with open('raw_data.txt', 'a+') as file:
                file.write("\nReceived At - {} Reading - {} Timestamp - {} Sensor Type - {}".format(datetime.datetime.now(),
                                                                                                 reading,
                                                                                                 timestamp,
                                                                                                 sensor_type))
            file.close()
            return

    def invalid_data(self, reading, timestamp, sensor_type):
        with open('invalid_data.txt', 'a+') as file:
            file.write(
                "\nReceived At - {} Reading - {} Timestamp - {} Sensor Type - {}".format(datetime.datetime.now(),
                                                                                      reading,
                                                                                      timestamp,
                                                                                      sensor_type))
            file.close()
        return
    def post(self, request):
        if request.META.get('HTTP_AUTHORIZATION') != settings.API_TOKEN:
            return HttpResponseForbidden()
        body = request.body.decode()
        payload = json.loads(body)
        reading = payload.get('reading')
        sensor_type = payload.get('sensorType')
        timestamp = payload.get('timestamp')
        try:
            validate(instance={"sensorType": sensor_type,
                               "reading": reading,
                               "timestamp": timestamp}, schema=self.validate_incoming_data())
        except jsonschema.ValidationError as ex:
            self.invalid_data(reading, timestamp, sensor_type)
        else:
            self.save_data(reading, timestamp, sensor_type)
        response= "Data has been recorded successfully."
        return HttpResponse(response, status=202)
