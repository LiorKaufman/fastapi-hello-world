FROM python:3.9-slim-buster


COPY ./app /app

COPY requirements.txt .
# install cron and R package dependencies
# RUN apt-get update && apt-get install -y \
#     cron \
#     nano \
#     tdsodbc \
#     odbc\
#     libsqliteodbc \
#     ## clean up
#     && apt-get clean \ 
#     && rm -rf /var/lib/apt/lists/ \ 
#     && rm -rf /tmp/downloaded_packages/ /tmp/*.rds

# RUN apt-get update \
#  && apt-get install --yes --no-install-recommends \
#         apt-transport-https \
#         curl \
#         gnupg \
#         unixodbc-dev \
#  && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#  && curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#  && apt-get update \
#  && ACCEPT_EULA=Y apt-get install --yes --no-install-recommends msodbcsql18 \
#  && apt-get clean \
#  && rm -rf /var/lib/apt/lists/* \
#  && rm -rf /tmp/*
# # RUN apt-get update \
# #   && apt-get -y install gcc \
# #   && apt-get -y install g++ \
# #   && apt-get -y install unixodbc unixodbc-dev \
# #   && apt-get clean
RUN pip3 install --user pyodbc
RUN pip --no-cache-dir install -r requirements.txt
WORKDIR /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]