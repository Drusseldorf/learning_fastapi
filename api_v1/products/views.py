from fastapi import APIRouter, status, Depends

from api_v1.products import crud
from api_v1.products.schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)
from api_v1.products.dependencies import product_by_id
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

router = APIRouter(tags=["Products"])


@router.get("")
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Product]:
    return await crud.get_products(session=session)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}")
async def get_product(product: Product = Depends(product_by_id)) -> Product:
    return product


@router.put("/{product_id}")
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency
    ),  # Fastapi кеширует зависимости, так что это будет тот же самый объект сессии из product_by_id
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update
    )


@router.patch("/{product_id}")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency
    ),  # Fastapi кеширует зависимости, так что это будет тот же самый объект сессии из product_by_id
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update, partial=True
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)
