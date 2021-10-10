from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from datetime import datetime, timedelta
import csv
import re
from os.path import exists


class Index(GenericAPIView):

    def get(self, request, *args, **kwargs):
        return render(request, 'simulator/chart.html')

    def post(self, request, *args, **kwargs):
        data = []
        start_time = request.data['startDatePicker']
        end_time = request.data['endDatePicker']

        start_time = re.findall(r"^\d{4}-\d{2}-\d{2}$", start_time)
        end_time = re.findall(r"^\d{4}-\d{2}-\d{2}$", end_time)

        if start_time == []:
            alarm = True
            state = "Start date must be provided"
            return render(request, 'simulator/chart.html', {"alarm": alarm, "state": state})

        if end_time == []:
            start_time = start_time.pop()
            end_time = start_time

        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        delta = timedelta(days=1)

        while start_time <= end_time:
            cur_time = start_time.strftime('%Y-%m-%d')
            if not exists(f'media/{cur_time}.csv'):
                alarm = True
                state = "File not found. Hint*(System time zone is not the same as the application)"
                return render(request, 'simulator/chart.html', {"alarm": alarm, "state": state})
            with open(f'media/{cur_time}.csv', 'rt') as f:
                reader = csv.reader(f)
                reader = [[int(row[0]) * 1000, int(row[1])] for row in reader if row]
                data += reader
            start_time += delta

        return render(request, 'simulator/chart.html', {"data": data})
