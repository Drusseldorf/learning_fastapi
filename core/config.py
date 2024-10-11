from pydantic_settings import BaseSettings


class Settigs(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = "postgresql+asyncpg://andrey:cfvjrfn@localhost:5432/learning_fastapi"
    db_echo: bool = True


settings = Settigs()
