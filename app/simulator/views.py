from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from datetime import datetime, timedelta
import csv
import re
from os.path import exists
from mobility.settings import TIME_ZONE
import pandas as pd


class Index(GenericAPIView):

    def get(self, request, *args, **kwargs):
        return render(request, 'simulator/chart.html', {"TIME_ZONE": TIME_ZONE})

    def post(self, request, *args, **kwargs):
        df = None
        statistics = {}

        start_time = request.data['startDatePicker']
        end_time = request.data['endDatePicker']

        start_time = re.findall(r"^\d{4}-\d{2}-\d{2}$", start_time)
        end_time = re.findall(r"^\d{4}-\d{2}-\d{2}$", end_time)

        if start_time == []:
            alarm = True
            state = "Start date must be provided"
            return render(request, 'simulator/chart.html', {"alarm": alarm, "state": state, "TIME_ZONE": TIME_ZONE})

        start_time = start_time.pop()
        if end_time == []:
            end_time = start_time
        else:
            end_time = end_time.pop()

        start_time = datetime.strptime(start_time, '%Y-%m-%d')
        end_time = datetime.strptime(end_time, '%Y-%m-%d')
        delta = timedelta(days=1)

        while start_time <= end_time:
            cur_time = start_time.strftime('%Y-%m-%d')
            if not exists(f'media/{cur_time}.csv'):
                alarm = True
                state = "File not found. Hint*(System time zone is not the same as the application)"
                return render(request, 'simulator/chart.html', {"alarm": alarm, "state": state, "TIME_ZONE": TIME_ZONE})
            df = pd.concat([df, pd.read_csv(f'media/{cur_time}.csv', header=None)])

            start_time += delta

        df[0] = df[0] * 1000
        statistics['count'] = df[1].describe()['count']
        statistics['mean'] = df[1].describe()['mean']
        statistics['min'] = df[1].describe()['min']
        statistics['max'] = df[1].describe()['max']
        statistics['std'] = df[1].describe()['std']

        return render(request, 'simulator/chart.html',
                      {"data": df.values.tolist(), "TIME_ZONE": TIME_ZONE, "statistics": statistics})
