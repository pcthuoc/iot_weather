# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from sensors.models import Sensors, SensorData
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from django.conf import settings
import requests
def index(request):
    sensors = Sensors.objects.all()

    # Lấy thứ hiện tại dạng tiếng Anh
    weekday_en = timezone.localtime().strftime('%a')  # e.g., 'Mon'

    # Mapping sang tiếng Việt
    weekday_map = {
        "Mon": "Thứ Hai",
        "Tue": "Thứ Ba",
        "Wed": "Thứ Tư",
        "Thu": "Thứ Năm",
        "Fri": "Thứ Sáu",
        "Sat": "Thứ Bảy",
        "Sun": "Chủ Nhật",
    }
    today = weekday_map.get(weekday_en, "")

    forecasts = [
        {"day": "Chủ Nhật", "status": "cloudy", "temp_max": 29, "temp_min": 26},
        {"day": "Thứ Hai", "status": "rainy", "temp_max": 29, "temp_min": 26},
        {"day": "Thứ Ba", "status": "sunny", "temp_max": 28, "temp_min": 26},
        {"day": "Thứ Tư", "status": "cloudy", "temp_max": 29, "temp_min": 26},
        {"day": "Thứ Năm", "status": "rainy", "temp_max": 28, "temp_min": 26},
        {"day": "Thứ Sáu", "status": "sunny", "temp_max": 29, "temp_min": 27},
        {"day": "Thứ Bảy", "status": "cloudy", "temp_max": 30, "temp_min": 27},
    ]
    hourly_forecasts = [
        {"time": "01:00", "temp": 27, "humidity": 82, "status": "cloudy", "wind": 12},
        {"time": "02:00", "temp": 26, "humidity": 85, "status": "rainy", "wind": 10},
        {"time": "03:00", "temp": 26, "humidity": 80, "status": "sunny", "wind": 8},
    ]
    context = {
        'segment': 'index',
        'sensors': sensors,
        'forecasts': forecasts,
        'today': today,
        'hourly_forecasts': hourly_forecasts,
    }

    html_template = loader.get_template('dashboard.html')
    return HttpResponse(html_template.render(context, request))
def sensor_chart_data(request):
    time_range = request.GET.get('range', '24h')

    time_map = {
        '1h': timedelta(hours=1),
        '3h': timedelta(hours=3),
        '6h': timedelta(hours=6),
        '12h': timedelta(hours=12),
        '24h': timedelta(hours=24),
        '3d': timedelta(days=3),
        '7d': timedelta(days=7),
    }

    duration = time_map.get(time_range, timedelta(hours=24))
    time_threshold = now() - duration

    data = {}
    sensors = Sensors.objects.all()

    for sensor in sensors:
        logs = SensorData.objects.filter(sensor_data=sensor, timestamp__gte=time_threshold)
        data[sensor.sensor_name] = [
            {
                'x': log.timestamp.isoformat(),
                'y': round(log.value, 1) if log.value % 1 != 0 else int(log.value)
            } for log in logs
        ]

    return JsonResponse(data)
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
