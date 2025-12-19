from fastapi import FastAPI, Depends, HTTPException, Query, Body
from typing import Annotated
from pydantic import BaseModel
from .inventory.inventory_service import InventoryService
from .inventory.inventory import InventorySummary, Inventory
from .inventory.inventory import ProductSummary
from .product.product import Product
from .product.product_service import ProductService
from .customError import NotFoundError, RemainingProductCountChangeError
from .dependencyContainer import get_inventory_service, get_product_service

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Inventory endpoints

@app.post("/v1/inventories")
async def create_inventory(service: Annotated[InventoryService, Depends(get_inventory_service)], 
                           name: str, 
                           location: str) -> str:
    return await service.create_inventory(name, location)

@app.get("/v1/inventories/{inventory_id}", response_model=Inventory)
async def get_inventory(service: Annotated[InventoryService, Depends(get_inventory_service)], inventory_id: str) -> Inventory:
    try:
        return await service.get_inventory(inventory_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
@app.get("/v1/inventories")
async def get_inventories(service: Annotated[InventoryService, Depends(get_inventory_service)],
                          include_category: Annotated[bool, Query()]=False) -> list[InventorySummary]:
    return await service.get_inventories(include_category=include_category)

@app.get("/v1/inventory/{inventory_id}/products", response_model=list[ProductSummary])
async def get_inventory_products(
    service: Annotated[InventoryService, Depends(get_inventory_service)],
    inventory_id: str,
    category: str | None = None
):
    try:
        return await service.get_existing_products(inventory_id, category)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)

@app.get("/v1/inventory/{inventory_id}/products/{product_id}/Count")
async def get_product_count(service: Annotated[InventoryService, Depends(get_inventory_service)],
                            inventory_id: str,
                            product_id: str) -> int:
    return await service.get_product_count(inventory_id, product_id)
    

class UpdateCountReqeust(BaseModel):
    quantity: int
    original_quantity: int | None = None
@app.post("/v1/inventory/{inventory_id}/products/{product_id}/Count")
async def update_product_count(
    service: Annotated[InventoryService, Depends(get_inventory_service)],
    inventory_id: str,
    product_id: str,
    updateCountRequest: Annotated[UpdateCountReqeust, Body()]) -> dict:
    try:
        result = await service.update_product_count(inventory_id, product_id, updateCountRequest.quantity, updateCountRequest.original_quantity)
        return {"success": result }
    except RemainingProductCountChangeError as e:
        return {"success": False, "new_count": e.newCount}



# Product endpoints

@app.post("/v1/products")
async def create_product(service: Annotated[ProductService, Depends(get_product_service)],
                         name: str, 
                         price: float, 
                         category: str,
                         description: str | None = None) -> str:
    product_id = await service.add_product(name=name, price=price, category=category, description=description)
    return product_id

@app.get("/v1/products/{product_id}", response_model=Product)
async def get_product(
    product_id: str,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    try:
        product = await service.get_product(product_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    return product