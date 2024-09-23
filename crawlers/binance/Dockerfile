FROM python:3.9-slim

WORKDIR /crawler/binance

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "crawl.py"]