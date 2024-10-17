from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User


class UserRelationMixin:
    _user_id_unique: bool = False
    _user_back_populates: str | None = None
    _user_id_nullable: bool = False

    # Классический прием, когда создается миксин для добавления отношения таблиц
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("user.id"),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship(
            "User",
            back_populates=cls._user_back_populates,  # Позволяет вам работать со связанными объектами как с атрибутами моделей
        )

        # ForeignKey создаёт связь на уровне базы данных.

        # relationship создаёт удобный интерфейс на уровне Python-объектов для работы с этой связью.
        # Соответственно этот код никак не влияет на фактические данные в БД
