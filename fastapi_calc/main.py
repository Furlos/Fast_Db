from fastapi import FastAPI
from core.models.db_helper import db_helper
from core.models.base import Base

Base.metadata.create_all(db_helper.engine)
app = FastAPI()
