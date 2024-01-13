from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+psycopg2://scott:tiger@localhost/scott"
    db_echo: bool = True


settings = Settings()
