import asyncio
import enum
from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text, ForeignKey, String

from core.config import settings

# Создание движка

# Синхронное подключение выполняется через create_engine
# Тут пример создания асинхронного движка и выполнение сырого sql запроса
# Можно обратить внимание на методы, вызываемые у результата
# Сам результат Представляет собой CursorResult object, по которому можно итерироваться
# У него можно вызвать методы например fist, all, one_or_none и другие, тут подробнее нужно читать документацию

engine = create_async_engine(
    url=settings.db.url,
    echo=True,
)


async def main():
    async with engine.connect() as conn:
        query = text(
            """
            Select 1+2;
            """
        )
        res = await conn.execute(query)
        print(res.one_or_none())


# asyncio.run(main())


#  Session , session_maker, запросы через orm

# Один раз конфигурируем создание сессии и будем переиспользовать
# Нужно создать модель данных
# Mapped позволяет задавать типы, по всей видимости для того чтобы статический анализатор понимал какой тип данных используется
# при этом в mapped_column уже не передаем тип, так как алхимия поймет это из Mapped
# При этом mapped_column можно вообще не указать, тогда просто никаких ограничений не наложится, будет чтото по умолчанию, скорее всего TEXT в субд.

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Worker(Base):
    __tablename__ = "worker"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]


worker_bober = Worker(username="Bober")


async def insert_worker_bober(session: AsyncSession):
    session.add(worker_bober)  # тут добавили в сессию, но еще не уходит в БД
    await session.commit()  # ушло в БД


session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def run_sql_funks():
    async with session_factory() as session:
        await insert_worker_bober(session=session)


#
# asyncio.run(run_sql_funks())
# print(worker_bober.username)


# Связи таблиц


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


# прием чтобы через анотейтед обозначить праймари кей
# Аналогично и для времени дефолтного, можно в общем таким образом повторяющийся код вынести.
intpk = Annotated[int, mapped_column(primary_key=True)]


class Resumes(Base):
    __tablename__ = "resume"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(256))  # ограничиваем длину строки
    compensation: Mapped[
        int | None
    ]  # допускаем None, можно и mapped_column(nullable=True)
    workload: Mapped[Workload]  # енамчик для бд
    worker_id: Mapped[int] = mapped_column(
        ForeignKey(
            "worker.id", ondelete="CASCADE"
        )  # при удалии воркера удаляется и резюме, хотя обычно на продакте так не делают
    )  # можно указать и модель, а не таблицу строкой,
    # но тогда нужно импортировать и можем попасть на рекурсивный импорт
    # ForeignKey создаёт связь на уровне базы данных. Влияет на БД

    # relationship создаёт удобный интерфейс на уровне Python-объектов для работы с этой связью.
    # Соответственно relationship никак не влияет на фактические данные в БД
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW()")
    )  # через server_default по умолчанию подставит данные,
    # если мы не указали это сами при инсерте. тут прописываем функцию Постгреса для приведения именно в utc
    # еще можно передать default чтобы туда передать datetime.utcnow(), для передачи именно из питон кода
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', NOW()"),
        onupdate=datetime.now(timezone.utc),
    )  # лучше это на уровне бд настроить самому


# Можно вынести ограничения

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}


# После кода выше мы можем в схемах теперь использовать ограничения через Annotated[str_256]


# Создать таблички не через алембик можно и так:


class SomeTable(Base):
    __tablename__ = "example"
    id: Mapped[intpk]
    some_atr: Mapped[str_256]


async def create_table_example():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# asyncio.run(create_table_example()) # создаст таблички
