from fastapi import FastAPI, HTTPException
from app.model import Predictor
from app.schemas import PenguinFeatures, PredictionResponse

# Создаём экземпляр приложения – ОБЯЗАТЕЛЬНО с именем app
app = FastAPI(title="Penguin Classifier API", version="1.0")

# Инициализируем предсказатель (загружает модель при старте)
predictor = Predictor()

@app.post("/predict", response_model=PredictionResponse)
async def predict(features: PenguinFeatures):
    """
    Эндпоинт для предсказания вида пингвина.
    Принимает JSON с признаками, возвращает предсказанный вид.
    """
    try:
        # Преобразуем Pydantic-модель в dict
        input_data = features.model_dump()
        species = predictor.predict(input_data)
        return PredictionResponse(species=species)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}

# Для локального запуска (необязательно)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)