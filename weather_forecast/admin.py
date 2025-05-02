from django.contrib import admin
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'temp', 'humidity', 'windspeed', 'precip', 'cloudcover')
    list_filter = ('precip', 'cloudcover', 'timestamp')
    search_fields = ('timestamp',)
    ordering = ('-timestamp',)
