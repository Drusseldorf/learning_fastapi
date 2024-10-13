from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import Base


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
