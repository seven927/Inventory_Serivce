from .product import Product
import json
import redis
from typing import Any

class ProductCache:
    def __init__(self):
        self.host = "redis-12289.c321.us-east-1-2.ec2.cloud.redislabs.com"
        self.port = 12289
        self.username="default"
        self.password="Dj5D96AYQExH2X6bJD4NpdI98AYnRPUM"
        
    async def get_product(self, product_id: str) -> Product | None:
        client = self.__getRedisClient()
        product_dict: Any
        try:
            product_dict = client.json().get(product_id)
        except Exception:
            raise Exception(f"An error occurred when getting prodcut {product_id} from Redis")
        finally:
            client.close()
        if(product_dict is None):
            return None
        return Product(id=product_dict["id"], name=product_dict["name"], price=product_dict["price"], category=product_dict["category"], description=product_dict["description"])
    async def add_product(self, product: Product)->bool:
        client = self.__getRedisClient()
        try:
            client.json().set(product.id, "$", product.model_dump())
        except Exception:
            raise Exception(f"An error occured when saving product {product.id} to Redis")
        finally:
            client.close()
        return True
    async def get_products(self, product_ids: list[str])->list[Product]:
        client = self.__getRedisClient()
        products_list = []
        products: list[Product] = []
        try:
            products_list = client.json().mget(product_ids, "$")
        except Exception :
            raise Exception(f"An error occurred when getting multiple products")
        finally:
            client.close()
        prd:Any
        for prd in products_list:
            if(prd is not None):
                products.append(Product(id=prd[0]["id"], name=prd[0]["name"], price=prd[0]["price"], category=prd[0]["category"], description=prd[0]["description"]))
        return products
    async def add_products(self, products: list[Product])->bool:
        client = self.__getRedisClient()
        products_dict: list[tuple[str, str, Any]] = []
        for product in products:
            products_dict.append((product.id, "$", product.model_dump()))
        try:
            client.json().mset(products_dict)
        except Exception as e:
            raise Exception(f"An error occurred when adding multiple products")
        finally:
            client.close()
        return True
    
    def __getRedisClient(self):
        return redis.Redis(
            host='redis-12289.c321.us-east-1-2.ec2.cloud.redislabs.com',
            port=12289,
            decode_responses=True,
            username="default",
            password="Dj5D96AYQExH2X6bJD4NpdI98AYnRPUM")