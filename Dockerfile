FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    fastapi uvicorn pandas numpy scikit-learn \
    python-dotenv sqlalchemy psycopg2-binary hvac aiokafka

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]