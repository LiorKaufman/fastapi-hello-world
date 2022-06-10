FROM python:3.9-slim


COPY ./app /app

COPY requirements.txt .
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean
RUN apt-get install python3-pip python3-dev 
RUN pip3 install --user pyodbc
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]