from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = (
        True  # causes declarative to skip the production of a table or mapper
    )
    # for the class entirely

    @classmethod  # This decorator never necessary from a runtime perspective,
    # however may be needed in order to support PEP 484 typing tools
    # that don’t otherwise recognize the decorated function as having class-level
    # behaviors for the cls parameter
    @declared_attr.directive  # automatically adding tablename by passing cls name
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # so we dont need to write id in orm models
