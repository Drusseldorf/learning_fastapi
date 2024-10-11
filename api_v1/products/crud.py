from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from core.models import Product
from api_v1.products.schemas import ProductCreate


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # Можно было бы сделать await session.refresh(product) это бы синхронизировало ОРМ объект с бд объектом
    # так как expire on commit - False
    # (после коммита, уже не гарантируется что ОРМ объект в оперативке соответствет тому
    # что лежит в бд)
    # объект будет в том состоянии в котором мы его сохраним,
    # а не идем за ним в БД дополнительно чтобы вернуть.
    # У нас асинхронное взаимодействие и это могут быть не самые актуальные данные
    return product
