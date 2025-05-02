from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Sensors(models.Model):
    updated_at = models.DateTimeField(default=timezone.now)  # Thời gian cập nhật, sử dụng giờ của Django
    sensor_id = models.CharField(max_length=255, unique=True)  # Định danh cảm biến (ID cảm biến)
    sensor_name = models.CharField(max_length=255)  # Tên cảm biến (ví dụ: Temperature, pH, etc.)
    value = models.FloatField(null=True, blank=True)  # Giá trị từ cảm biến, có thể để trống
    unit = models.CharField(max_length=50, null=True, blank=True)  # Đơn vị đo, có thể để trống
    save_at = models.DateTimeField(default=timezone.now) 

    def save(self, *args, **kwargs):
        # Kiểm tra nếu sensor_id đã tồn tại, chỉ cập nhật nếu tồn tại
        if self.pk is None:  # Nếu là bản ghi mới, không cần kiểm tra
            existing_sensor = Sensors.objects.filter(sensor_id=self.sensor_id).first()  # Sửa lại model là Sensors
            if existing_sensor:
                # Nếu cảm biến đã tồn tại, chỉ cập nhật giá trị mà không tạo mới
                self.pk = existing_sensor.pk  # Đặt khóa chính để cập nhật
                self.updated_at = timezone.now()  # Cập nhật thời gian
        super(Sensors, self).save(*args, **kwargs)  # Gọi phương thức save của lớp cha

    def __str__(self):
        return f"{self.sensor_name} ({self.sensor_id}) - {self.value} {self.unit} at {self.updated_at}"

    class Meta:
        verbose_name = "Sensors"
        verbose_name_plural = "Sensors"
        
class SensorData(models.Model):
    sensor_data = models.ForeignKey(Sensors, on_delete=models.CASCADE)  # Liên kết với SensorData, xóa tự động khi xóa SensorData
    value = models.FloatField()  # Giá trị cảm biến theo thời gian
    timestamp = models.DateTimeField(default=timezone.now)  # Thời gian đo giá trị cảm biến

    def __str__(self):
        return f"{self.sensor_data.sensor_name} - {self.value} {self.sensor_data.unit} at {self.timestamp}"

    class Meta:
        verbose_name = "Sensor Data"
        verbose_name_plural = "Sensor Data"
