FROM python:3.9-slim


COPY ./app /app

COPY requirements.txt .
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean
RUN pip3 install --user pyodbc
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]