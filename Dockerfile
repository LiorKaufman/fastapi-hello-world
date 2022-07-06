FROM python:3.9-slim-buster


COPY ./app /app

COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt
WORKDIR /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]