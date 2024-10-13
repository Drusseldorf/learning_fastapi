from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from core.models.base import Base

# Специальный флаг, который вернет False в момент рантайма,
# но для тайпчекинга мы сможем импортировать модель, и это не помешает в рантайме
if TYPE_CHECKING:
    from .user import User


class Post(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",  # дефолт для алхимии, объекты в пользовательском коде
        server_default="",  # дефолт для субд, на уровне субд вешается дефолтное значение
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user.id"
        ),  # вобще говоря можно передать в аргумент непосредственно модель
        # и ее атрибут User.id, но тогда у нас будут циклические импорты
    )
    # ForeignKey создаёт связь на уровне базы данных.
    # relationship создаёт удобный интерфейс на уровне Python-объектов для работы с этой связью.
    # Соответственно этот код никак не влияет на фактические данные в БД
    user: Mapped["User"] = relationship(back_populates="post")
