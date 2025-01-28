FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ANTHROPIC_API_KEY=""
ENV BACKEND_URL="http://backend:8000/api"

CMD ["python", "app.py"] 