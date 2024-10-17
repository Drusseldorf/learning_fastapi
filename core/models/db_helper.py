from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # echo - if True, the Engine will log all statements as well as a repr() of their parameter lists to the default log handler,
        # which defaults to sys.stdout for output
        # on prod must set to False
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # When True, all query operations will issue a Session.flush() call to this Session before proceeding.
            # This is a convenience feature so that Session.flush() need not be called repeatedly in order for database queries to retrieve results
            autocommit=False,  # обычно все False, чтобы вручную управлять этим. (по умолчанию False): если True, сессия автоматически коммитит изменения после каждого запроса
            expire_on_commit=False,  # Defaults to True. When True, all instances will be fully expired after each commit(),
            # so that all attribute/object access subsequent to a completed transaction will load from the most recent database state
            # (по умолчанию True): если установлено в True, все объекты, связанные с этой сессией, будут помечены как "устаревшие" после вызова commit. Это значит,
            # что при следующем доступе к атрибутам этих объектов,
            # сессия автоматически выполнит повторный запрос к базе данных,
            # чтобы получить их актуальные данные. Если установить в False,
            # то объекты сохранят свои данные после коммита, что может быть полезно,
            # если вы не хотите лишних запросов. Но при этом не гарантируется их актуальность
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,  # async_scoped_session создаёт "скоупированную" сессию,
            # что значит, что одна и та же сессия будет использоваться в пределах определённого контекста,
            # который задается функцией scopefunc. В асинхронных приложениях,
            # таких как FastAPI, это полезно для того, чтобы обеспечить,
            # что каждая асинхронная задача (asyncio task) получает свою собственную сессию.
        )
        return session

    # асинхронный генератор, который используется для предоставления сессии как зависимости
    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        # await session.close()  # На самом деле тут это не нужно,
        # так как используетсяa sync_scoped_session, то
        # сессия закрывается когда завершается асинхронная таска.


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
