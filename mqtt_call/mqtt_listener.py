import paho.mqtt.client as mqtt
import threading
import queue
import json
from django.utils import timezone
from sensors.models import Sensors,SensorData
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings  # ✅ import settings Django


# Hàng đợi xử lý tin nhắn MQTT
mqtt_message_queue = queue.Queue()

# Callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected successfully.")
        client.subscribe(settings.MQTT_TOPIC)
    else:
        print(f"[MQTT] Connection failed with code {rc}")

# Callback khi nhận được tin nhắn MQTT
def on_message(client, userdata, msg):
    try:
        mqtt_message_queue.put(msg)
        print(f"[MQTT] Message received from topic: {msg.topic}")
    except Exception as e:
        print(f"[ERROR] Failed to enqueue MQTT message: {e}")

def process_mqtt_queue(client):
    while True:
        try:
            msg = mqtt_message_queue.get()
            topic_parts = msg.topic.split('/')

            if len(topic_parts) == 2 and topic_parts[0] == "IOT":
                sensor_id = "sensor_" + topic_parts[1]
                payload = msg.payload.decode("utf-8")

                # Giải mã payload
                try:
                    data = json.loads(payload)
                    rvalue = float(data.get("value"))
                    value = rvalue  # ✅ Sửa lỗi ở đây
                except Exception:
                    value = float(payload)
                    print(f"[WARNING] Payload không phải JSON hợp lệ: {payload}")

                if value is None:
                    print(f"[ERROR] Không xử lý được dữ liệu từ '{sensor_id}'")
                    mqtt_message_queue.task_done()
                    continue

                # Truy xuất DB
                sensor = Sensors.objects.filter(sensor_id=sensor_id).first()
                if sensor:
                    time_diff = timezone.now() - sensor.save_at
                    print(f"[INFO] Thời gian cập nhật cuối: {sensor.save_at}, thời gian chênh lệch: {time_diff.total_seconds()} giây")
                    if time_diff.total_seconds() > settings.TIME_SAVE*60:
                        print("luu lại dữ liệu vào DB")
                        SensorData.objects.create(
                            sensor_data=sensor,
                            value=value,
                            timestamp=timezone.now()
                        )

                        sensor.save_at = timezone.now()

                    sensor.value = value
                    sensor.updated_at = timezone.now()
                    unit= sensor.unit
                    sensor.save()

                    # Gửi WebSocket
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "sensor_data",
                        {
                            "type": "send_sensor_data",
                            "sensor_id": sensor_id,
                            "value": value,
                            "unit": unit,
                            "updated_at": timezone.now().isoformat()
                        }
                    )
                else:
                    print(f"[INFO] Sensor '{sensor_id}' không tồn tại trong DB.")
            else:
                print(f"[WARNING] Cấu trúc topic sai: {msg.topic}")

            mqtt_message_queue.task_done()

        except Exception as e:
            print(f"[ERROR] Lỗi khi xử lý MQTT message: {e}")


# Khởi động client MQTT và thread hàng đợi
def start_mqtt_listener():
    client = mqtt.Client()
    client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
        client.loop_start()

        # Khởi động thread xử lý hàng đợi
        processing_thread = threading.Thread(target=process_mqtt_queue, args=(client,))

        processing_thread.daemon = True
        processing_thread.start()

        print("[MQTT] Listener and queue processor started.")
    except Exception as e:
        print(f"[ERROR] Failed to start MQTT client: {e}")