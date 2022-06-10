FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

COPY requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]