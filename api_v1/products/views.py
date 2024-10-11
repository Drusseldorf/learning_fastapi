from fastapi import APIRouter, HTTPException, status, Depends
from api_v1.products import crud
from api_v1.products.schemas import Product, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

router = APIRouter(tags=["Products"])


@router.get("")
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[Product]:
    return await crud.get_products(session=session)


@router.post("")
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}")
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product | None:
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found",
    )
