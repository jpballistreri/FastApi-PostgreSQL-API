from sqlalchemy import create_engine, MetaData

import os
from dotenv import load_dotenv

load_dotenv()

URL_POSTGRES = f'postgresql://{os.getenv("YOUR_DATABASE_USER")}:{os.getenv("YOUR_DATABASE_PASSWORD")}@localhost:5432/{os.getenv("YOUR_DATABASE_NAME")}'

engine = create_engine(
    URL_POSTGRES, isolation_level='AUTOCOMMIT')

meta = MetaData()
conn = engine.connect()
