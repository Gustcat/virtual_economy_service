FROM python:3.11-slim

WORKDIR /wrk

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uvicorn app.main:app --host $HTTP_HOST --port $HTTP_PORT