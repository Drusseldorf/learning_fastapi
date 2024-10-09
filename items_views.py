from typing import Annotated
from fastapi import Path, APIRouter

router = APIRouter(
    prefix="/items", tags=["Items"]  # tag to group up views in swagger
)  # Namespaces are one honking great idea!


@router.get("")
def list_items():
    return ["Item1", "Item2"]


@router.get("/latest")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}


@router.get("/{item_id}")  # var as a path
def get_item_by_id(
    item_id: Annotated[int, Path(ge=1, lt=1_000_000)]
):  # Annotated for validating value. First one is type, second is a special fastapi obj that allows to pass constraits
    return {"item": {"id": item_id}}
