from django.contrib import admin
from .models import Sensors, SensorData

class SensorsAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'sensor_name', 'value', 'unit', 'updated_at')
    search_fields = ('sensor_id', 'sensor_name')
    list_filter = ('unit',)
    ordering = ('-updated_at',)

# Đăng ký model Sensors với admin
admin.site.register(Sensors, SensorsAdmin)

class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('sensor_data', 'value', 'timestamp')  # Các cột hiển thị trong danh sách
    search_fields = ('sensor_data__sensor_id', 'sensor_data__sensor_name')  # Tìm kiếm theo sensor_id và sensor_name
    list_filter = ('sensor_data__sensor_name',)  # Bộ lọc theo tên cảm biến
    ordering = ('-timestamp',)  # Sắp xếp theo thời gian đo, mới nhất lên trên

    # Sử dụng form để chọn cảm biến
    fieldsets = (
        (None, {
            'fields': ('sensor_data', 'value', 'timestamp'),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tự động điền dữ liệu cho trường foreign key sensor_data, chỉ hiển thị cảm biến đang có dữ liệu trong bảng SensorData
        if db_field.name == "sensor_data":
            kwargs["queryset"] = Sensors.objects.all()  # Lấy tất cả cảm biến từ model Sensors
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Đăng ký model SensorData với admin
admin.site.register(SensorData, SensorDataAdmin)
