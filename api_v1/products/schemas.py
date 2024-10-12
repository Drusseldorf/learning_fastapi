from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, conint
from typing import Annotated


class ProductBase(BaseModel):
    name: str
    description: str
    price: Annotated[int, conint(ge=1, le=1_000_000)]


class ProductCreate(ProductBase):  # we dont want users to send us id to create product,
    # it has autoinctr in db
    pass


class ProductUpdate(ProductBase):
    pass


class ProductUpdatePartial(ProductBase):
    name: str | None = None
    description: str | None = None
    price: Annotated[int, conint(ge=1, le=1_000_000)] | None = None


class Product(ProductBase):  # it will be return to users, with id
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, conint(ge=1, le=1_000_000)]
