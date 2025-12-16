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
        product_str: Any
        try:
            product_str = client.get(product_id)
        except Exception:
            raise Exception(f"An error occurred when getting prodcut {product_id} from Redis")
        finally:
            client.close()
        if(product_str is None):
            return None
        product_dict = json.loads(product_str)
        return Product(id=product_dict["id"], name=product_dict["name"], price=product_dict["price"], category=product_dict["category"])
    async def add_product(self, product: Product)->bool:
        product_str = json.dumps(product, default=lambda o: o.__dict__)
        client = self.__getRedisClient()
        try:
            client.set(product.id, product_str)
        except Exception:
            raise Exception(f"An error occured when saving product {product.id} to Redis")
        finally:
            client.close()
        return True
    async def get_products(self, product_ids: list[str])->list[Product]:
        client = self.__getRedisClient()
        products_str = []
        products: list[Product] = []
        try:
            products_str = client.mget(product_ids)
        except Exception :
            raise Exception(f"An error occurred when getting multiple products")
        finally:
            client.close()
        for prd in products_str:
            product_dict = json.loads(prd)
            products.append(Product(id=product_dict["id"], name=product_dict["name"], price=product_dict["price"], category=product_dict["category"]))
        return products
    async def add_products(self, products: list[Product])->bool:
        client = self.__getRedisClient()
        products_str: dict[str, str] = dict()
        for product in products:
            products_str[product.id]=json.dumps(product, default=lambda o: o.__dict__)
        try:
            client.mset(products_str)
        except Exception:
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