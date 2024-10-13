from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from core.models.base import Base
from typing import TYPE_CHECKING

from core.models.profile import Profile

# Специальный флаг, который вернет False в момент рантайма, но True при статическом аналие кода
# но для тайпчекинга мы сможем импортировать модель, и это не помешает в рантайме
if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    # ForeignKey создаёт связь на уровне базы данных.
    # relationship создаёт удобный интерфейс на уровне Python-объектов для работы с этой связью.
    # Соответственно этот код никак не влияет на фактические данные в БД
    # У нас тут лист от Post, ибо отношение 1 ко многим, у юзера может быть много постов
    post: Mapped[list["Post"]] = relationship(back_populates="user")

    profile: Mapped["Profile"] = relationship(back_populates="user")
