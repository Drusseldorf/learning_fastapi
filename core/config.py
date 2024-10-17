from pydantic_settings import BaseSettings
from pydantic import BaseModel


class DbSettiongs(BaseModel):
    url: str = "postgresql+asyncpg://andrey:cfvjrfn@localhost:5432/learning_fastapi"
    echo: bool = True


class Settigs(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettiongs = DbSettiongs()


settings = Settigs()
