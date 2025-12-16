from ..product.product import Product
from ..product.product_service import ProductService
from .inventory import InventorySummary, ProductSummary, Inventory
from .inventory_repository import InventoryRepository
from ..customError import RemainingProductCountChangeError

def get_inventory_repository():
    return InventoryRepository()

def get_product_service():
    return 

class InventoryService:
    def __init__(self, 
                 respository: InventoryRepository,
                 product_service: ProductService):
        self.inventories = []
        self.repository = respository
        self.product_service = product_service
    async def create_inventory(self, name: str, location: str) -> str:
        return await self.repository.add_inventory(name, location)
    
    async def get_inventory(self, inventory_id: str) -> Inventory:
        return await self.repository.get_inventory(inventory_id)

    async def get_inventories(self, include_category: bool = False) -> list[InventorySummary]:
        inventory_list = []
        inventories = await self.repository.get_inventories()
        for inventory in inventories:
            if include_category:
                category_set = set()
                if inventory.products is not None:
                    for item in inventory.products.items():
                        category = await self.__get_product_category(item[0])
                        category_set.add(category)
                inventory_list.append(InventorySummary(id=inventory.id, name=inventory.name, location=inventory.location, categories= list(category_set)))
            else:
                inventory_list.append(InventorySummary(id=inventory.id, name=inventory.name, location=inventory.location))
        return inventory_list    

    async def get_existing_products(self, inventory_id: str, category: str | None = None) -> list[ProductSummary]:
        inventory = await self.repository.get_inventory(inventory_id)
        product_list = []
        if inventory.products is not None:
            id_list = list(inventory.products.keys())
            products = await self.product_service.get_products(id_list)
            for product in products:
                if category is not None:
                    if product.category == category:
                        product_list.append(ProductSummary(id=product.id, name=product.name, price=product.price, category=product.category, count=inventory.products[product.id]))
                else:
                    product_list.append(ProductSummary(id=product.id, name=product.name, price=product.price, category=product.category, count=inventory.products[product.id]))
        return product_list        
    
    async def update_product_count(self, inventory_id: str, product_id: str, quantity: int, original_quantity: int | None = None) -> bool:
        new_count = await self.get_product_count(inventory_id, product_id)
        if original_quantity != None and new_count >= 0 and new_count != original_quantity:
            raise RemainingProductCountChangeError(new_count)
        return await self.repository.update_product_count(inventory_id, product_id, quantity, new_count==-2)
    
    async def get_product_count(self, inventory_id: str, product_id: str) -> int:
        inventory = await self.repository.get_inventory(inventory_id)
        if inventory.products is None:
            return -2
        if product_id in inventory.products:
            return inventory.products[product_id]
        return -1
    
    async def __get_product_category(self, product_id: str) -> str:
        product = await self.product_service.get_product(product_id)
        return product.category
        