FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY download_models.py .
RUN python download_models.py /pipeline_models

COPY main.py .
COPY src/ /app/src/

ENTRYPOINT ["python", "main.py"]