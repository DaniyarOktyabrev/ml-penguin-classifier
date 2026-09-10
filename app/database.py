import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Check your .env file.")

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    island = Column(String, nullable=False)
    bill_length_mm = Column(Float, nullable=False)
    bill_depth_mm = Column(Float, nullable=False)
    flipper_length_mm = Column(Float, nullable=False)
    body_mass_g = Column(Float, nullable=False)
    sex = Column(String, nullable=False)
    species = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


def init_db():
    """Создаёт таблицы, если их нет."""
    Base.metadata.create_all(bind=engine)


def save_prediction(input_data: dict, species: str) -> None:
    """Сохраняет предсказание в БД."""
    session = SessionLocal()
    try:
        record = Prediction(
            island=input_data["island"],
            bill_length_mm=input_data["bill_length_mm"],
            bill_depth_mm=input_data["bill_depth_mm"],
            flipper_length_mm=input_data["flipper_length_mm"],
            body_mass_g=input_data["body_mass_g"],
            sex=input_data["sex"],
            species=species,
        )
        session.add(record)
        session.commit()
    finally:
        session.close()


def get_recent_predictions(limit: int = 50):
    """Возвращает последние N предсказаний."""
    session = SessionLocal()
    try:
        records = (
            session.query(Prediction)
            .order_by(Prediction.id.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": r.id,
                "island": r.island,
                "species": r.species,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ]
    finally:
        session.close()