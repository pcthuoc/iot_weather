from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    CLOUD_CHOICES = [
        ('sunny', 'Nắng'),
        ('cloudy', 'Mây'),
    ]

    PRECIP_CHOICES = [
        ('rain', 'Mưa'),
        ('no_rain', 'Không mưa'),
    ]

    timestamp = models.DateTimeField(default=timezone.now)  # Lấy giờ theo Django TIME_ZONE
    temp = models.FloatField()
    humidity = models.FloatField()
    windspeed = models.FloatField()
    precip = models.CharField(max_length=10, choices=PRECIP_CHOICES)
    cloudcover = models.CharField(max_length=10, choices=CLOUD_CHOICES)

    def __str__(self):
        return f"Weather at {self.timestamp}"


class WeatherPrediction(models.Model):
    CLOUD_CHOICES = [
        ('sunny', 'Nắng'),
        ('cloudy', 'Mây'),
    ]

    PRECIP_CHOICES = [
        ('rain', 'Mưa'),
        ('no_rain', 'Không mưa'),
    ]

    # Không có thời gian nữa, chỉ lưu giá trị dự đoán
    temp = models.FloatField()
    humidity = models.FloatField()
    windspeed = models.FloatField()
    precip = models.CharField(max_length=10, choices=PRECIP_CHOICES)
    cloudcover = models.CharField(max_length=10, choices=CLOUD_CHOICES)

    def __str__(self):
        return f"Weather Prediction (3h ahead)"