FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    net-tools \
    iproute2 \
    wireless-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements & setup
COPY backend/ /app/backend/
COPY ml/ /app/ml/
COPY scripts/ /app/scripts/
COPY .env.example /app/.env

WORKDIR /app/backend
RUN pip install --no-cache-dir -r <(echo -e "fastapi\nuvicorn\npydantic\npydantic-settings\nemail-validator\nsqlalchemy\npsycopg2-binary\nalembic\npython-jose[cryptography]\nbcrypt\nrequests\nscikit-learn\npandas\nnumpy\njoblib\npytest\nhttpx")

ENV PYTHONPATH="/app:/app/backend"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
