FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

COPY requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt
RUN uvicorn main:app  