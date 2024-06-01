 
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ src/
COPY models/ models/
COPY data/ data/

CMD ["python", "src/monitor_traffic.py"]
