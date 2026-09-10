from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.model import Predictor
from app.schemas import PenguinFeatures, PredictionResponse
from app.database import init_db, save_prediction, get_recent_predictions


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация БД при старте."""
    init_db()
    yield


app = FastAPI(title="Penguin Classifier API", version="2.0", lifespan=lifespan)
predictor = Predictor()


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: PenguinFeatures):
    try:
        input_data = features.model_dump()
        species = predictor.predict(input_data)
        save_prediction(input_data, species)
        return PredictionResponse(species=species)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/predictions")
async def predictions():
    """Возвращает последние 50 предсказаний из БД."""
    return get_recent_predictions(50)