from pydantic_settings import BaseSettings


class Settigs(BaseSettings):
    db_url: str = "postgresql+asyncpg://andrey:cfvjrfn@localhost:5432/learning_fastapi"
    db_echo: bool = True


settings = Settigs()
