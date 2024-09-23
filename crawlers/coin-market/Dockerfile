# parent image
FROM python:3.9-slim

WORKDIR /crawler/coin-market

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# run app.py upon container launch
CMD ["python", "crawl.py"]