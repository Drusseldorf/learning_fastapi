from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import Base
from .mixins import UserRelationMixin

# Специальный флаг, который вернет False в момент рантайма,
# но для тайпчекинга мы сможем импортировать модель, и это не помешает в рантайме


class Post(UserRelationMixin, Base):
    # Уже по умолчанию False в миксине
    # _user_id_nullable = False
    # _user_id_unique = False

    _user_back_populates = "post"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",  # дефолт для алхимии, объекты в пользовательском коде
        server_default="",  # дефолт для субд, на уровне субд вешается дефолтное значение
    )
