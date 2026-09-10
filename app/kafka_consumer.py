import json
import asyncio
from aiokafka import AIOKafkaConsumer
from app.database import save_prediction

class KafkaConsumerService:
    def __init__(self, bootstrap_servers: str, topic: str, group_id: str = "penguin-group"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        self._task = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        print(f"[Kafka] Consumer subscribed to '{self.topic}'")
        self._task = asyncio.create_task(self._consume_loop())

    async def _consume_loop(self):
        try:
            async for msg in self.consumer:
                print(f"[Kafka] Received: {msg.value}")
                try:
                    save_prediction(msg.value, msg.value["species"])
                except Exception as e:
                    print(f"[Kafka] Error saving to DB: {e}")
        except asyncio.CancelledError:
            pass

    async def stop(self):
        if self._task:
            self._task.cancel()
        if self.consumer:
            await self.consumer.stop()
            print("[Kafka] Consumer stopped")