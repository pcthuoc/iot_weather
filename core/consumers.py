# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from sensors.models import Sensors


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "sensor_data"  # ✅ Tất cả đều vào group chung
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print("[WS] Client connected to group: sensor_data")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("[WS] Client disconnected")

    async def receive(self, text_data):
        print("[WS] Received from client:", text_data)
        # Bạn có thể xử lý thêm nếu cần

    async def send_sensor_data(self, event):
        await self.send(text_data=json.dumps({
            "sensor_id": event["sensor_id"],
            "value": event["value"],
            "unit": event["unit"],
            "updated_at": event["updated_at"]
        }))