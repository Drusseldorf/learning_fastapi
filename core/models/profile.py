from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from core.models.base import Base
from typing import TYPE_CHECKING

from .mixins import UserRelationMixin

# Специальный флаг, который вернет False в момент рантайма, но True при статическом аналие кода
# но для тайпчекинга мы сможем импортировать модель, и это не помешает в рантайме


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None]
