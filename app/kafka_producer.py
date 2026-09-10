import json
import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

class KafkaProducerService:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None

    async def start(self, retries: int = 10, delay: int = 5):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        for attempt in range(1, retries + 1):
            try:
                await self.producer.start()
                print(f"[Kafka] Producer connected to {self.bootstrap_servers}")
                return
            except KafkaConnectionError as e:
                print(f"[Kafka] Producer attempt {attempt}/{retries}: {e}")
                await asyncio.sleep(delay)
        raise RuntimeError("Could not start Kafka producer")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            print("[Kafka] Producer stopped")

    async def send(self, message: dict):
        if not self.producer:
            raise RuntimeError("Producer is not started")
        await self.producer.send_and_wait(self.topic, message)
        print(f"[Kafka] Message sent: {message}")