FROM python:3.9-slim

WORKDIR /starheroes

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY config.py .

COPY run.py .

EXPOSE 5000

CMD ["python", "run.py"]
