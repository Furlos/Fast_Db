from sqlalchemy import create_engine

from core.config import settings


class DataBaseHelper:
    def __init__(self):
        self.engine = create_engine(
            url=settings.db_url,
            echo=settings.db_echo,
        )

db_helper = DataBaseHelper()
