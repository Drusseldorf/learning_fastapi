from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from core.models.base import Base
from typing import TYPE_CHECKING

# Специальный флаг, который вернет False в момент рантайма, но True при статическом аналие кода
# но для тайпчекинга мы сможем импортировать модель, и это не помешает в рантайме
if TYPE_CHECKING:
    from .post import Post


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    # ForeignKey создаёт связь на уровне базы данных.
    # relationship создаёт удобный интерфейс на уровне Python-объектов для работы с этой связью.
    # Соответственно этот код никак не влияет на фактические данные в БД
    post: Mapped[list["Post"]] = relationship(back_populates="user")
