FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN pip install --no-cache-dir "psycopg[binary]==3.3.6"

COPY seeds/seed.py ./seeds/seed.py
COPY sql/models/model.sql ./sql/models/model.sql

CMD ["python", "seeds/seed.py", "--init-schema", "--if-empty"]
