from fastapi import Depends
from typing import Annotated
from .inventory.inventory_service import InventoryService
from .inventory.inventory_repository import InventoryRepository
from .product.product_service import ProductService
from .product.product_repository import ProductRepository
from .product.product_cache import ProductCache

def get_inventory_repository():
    return InventoryRepository()

def get_product_reporsitory():
    return ProductRepository()

def get_prodcut_cache():
    return ProductCache()

def get_product_service(repo: Annotated[ProductRepository, Depends(get_product_reporsitory)],
                        cache: Annotated[ProductCache, Depends(get_prodcut_cache)]):
    return ProductService(repo, cache)


def get_inventory_service(repo: Annotated[InventoryRepository, Depends(get_inventory_repository)], 
                          service: Annotated[ProductService, Depends(get_product_service)]) -> InventoryService:
    return InventoryService(repo, service)


