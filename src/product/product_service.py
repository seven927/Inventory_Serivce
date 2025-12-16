from .product import Product
from .product_repository import ProductRepository
from .product_cache import ProductCache

class ProductService:
    def __init__(self, respository: ProductRepository, cache: ProductCache):
        self.repository = respository
        self.cache = cache
    
    async def add_product(self, name: str, price: float, category: str, description: str | None = None) -> str:
        return await self.repository.add_product(name, price, category, description)

    async def get_product(self, product_id: str) -> Product:
        cachedResult = await self.cache.get_product(product_id)
        if(cachedResult!=None):
            return cachedResult
        result = await self.repository.get_product(product_id)
        await self.cache.add_product(result)
        return result
    async def get_products(self, product_ids: list[str]) -> list[Product]:
        cacheResult = await self.cache.get_products(product_ids)
        requestList = []
        if(cacheResult == None or len(cacheResult) == 0):
            requestList = product_ids
        else:
            id_set = set()
            for product in cacheResult:
                id_set.add(product.id)
            for id in product_ids:
                if(id not in id_set):
                    requestList.append(id)
        if len(requestList)==0:
            return cacheResult
        new_list = await self.repository.get_products(requestList)
        await self.cache.add_products(new_list)
        if(cacheResult is not None):
            new_list.extend(cacheResult)
        return new_list