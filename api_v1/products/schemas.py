from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):  # we dont want users to send us id to create product,
    # it has autoinctr in db
    pass


class Product(ProductBase):  # it will be return to users, with id
    model_config = ConfigDict(from_attributes=True)

    id: int
