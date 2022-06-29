from sqlalchemy import event
from azure.identity import DefaultAzureCredential
import struct
from sqlalchemy.engine import URL
import os
from sqlmodel import Session,create_engine

credential = DefaultAzureCredential()
databaseToken = credential.get_token('https://database.windows.net/')

# get bytes from token obtained
tokenb = bytes(databaseToken[0], "UTF-8")
exptoken = b'';
for i in tokenb:
    exptoken += bytes({i});
    exptoken += bytes(1);
tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;

server = os.getenv("SERVER_NAME")
database = os.getenv("DATABASE")
# build connection string using acquired token
connString = "Driver={ODBC Driver 18 for SQL Server};SERVER="+server+";DATABASE="+database+""
SQL_COPT_SS_ACCESS_TOKEN = 1256 
# conn = pyodbc.connect(connString, attrs_before = {SQL_COPT_SS_ACCESS_TOKEN:tokenstruct});
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connString})
engine = create_engine(connection_url)
session = Session(bind=engine)
@event.listens_for(engine, "do_connect")
def provide_token(dialect, conn_rec, cargs, cparams):
    # remove the "Trusted_Connection" parameter that SQLAlchemy adds
    cargs[0] = cargs[0].replace(";Trusted_Connection=Yes", "")

    # create token credential
    raw_token = credential.get_token('https://database.windows.net/').token.encode("utf-16-le")
    token_struct = struct.pack(f"<I{len(raw_token)}s", len(raw_token), raw_token)

    # apply it to keyword arguments
    cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}

def get_db_engine():
    return engine