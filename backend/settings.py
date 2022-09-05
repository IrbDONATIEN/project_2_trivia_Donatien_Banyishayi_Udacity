import os
from dotenv import load_dotenv

load=load_dotenv()

#Connection to Database trivia:
DB_NAME = os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
HOST_NAME=os.environ.get("HOST_NAME")

#Connection to Database  trivia_test:
DB_NAME1 = os.environ.get("DB_NAME1")
DB_USER1=os.environ.get("DB_USER1")
DB_PASSWORD1 = os.environ.get("DB_PASSWORD1")
HOST_NAME1=os.environ.get("HOST_NAME1")