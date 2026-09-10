from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.model import Predictor
from app.schemas import PenguinFeatures, PredictionResponse
from app.database import init_db, get_recent_predictions
from app.secrets import get_kafka_config
from app.kafka_producer import KafkaProducerService
from app.kafka_consumer import KafkaConsumerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация БД
    init_db()

    # Получаем Kafka-конфигурацию из Vault
    kafka_config = get_kafka_config()

    # Запуск Producer и Consumer
    producer = KafkaProducerService(
        kafka_config["bootstrap_servers"],
        kafka_config["topic"],
    )
    consumer = KafkaConsumerService(
        kafka_config["bootstrap_servers"],
        kafka_config["topic"],
    )
    await producer.start()
    await consumer.start()

    app.state.producer = producer

    yield

    await consumer.stop()
    await producer.stop()


app = FastAPI(title="Penguin Classifier API", version="3.0", lifespan=lifespan)
predictor = Predictor()


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: PenguinFeatures):
    try:
        input_data = features.model_dump()
        species = predictor.predict(input_data)

        # Отправляем в Kafka
        message = {**input_data, "species": species}
        await app.state.producer.send(message)

        return PredictionResponse(species=species)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/predictions")
async def predictions():
    return get_recent_predictions(50)