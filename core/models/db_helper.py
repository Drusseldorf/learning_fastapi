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
            autocommit=False,
            expire_on_commit=False,  # Defaults to True. When True, all instances will be fully expired after each commit(),
            # so that all attribute/object access subsequent to a completed transaction will load from the most recent database state.
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)
