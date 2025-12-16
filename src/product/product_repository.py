from .product import Product
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
from ..customError import NotFoundError
from typing import Any
from bson.objectid import ObjectId

class ProductRepository:
    def __init__(self):
        self.url = "mongodb+srv://eacmomo0927_db_user:vKaA49hxWXGLdVe8@mycluster.9cvhjpt.mongodb.net/?appName=MyCluster"
    async def get_product(self, product_id: str) -> Product:
        client: AsyncMongoClient[dict[str, Any]] | None = None
        result: Any
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = await db["product"].find_one({"_id": ObjectId(product_id)})
        except Exception as e:
            raise Exception(f"An error occurred when getting prodcut {product_id} : {e}")
        finally:
            if client is not None:
                await client.close()
        if(result is None):
            raise NotFoundError(f"Product with {product_id} not found")
        return Product(id=str(result["_id"]), name=result["name"], price=result["price"], category=result["category"], description=result["description"])

    async def add_product(self, name: str, price: float, category: str, description: str | None = None) -> str:
        client: AsyncMongoClient[dict[str, Any]] | None = None
        result: InsertOneResult | None = None
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = await db["product"].insert_one({"name": name, "price": price, "category": category, "description": description})
        except Exception as e:
            raise Exception(f"An error occurred when creating product for {name}: {e}")
        finally:
            if client is not None:
                await client.close()
        return str(result.inserted_id)

        
    async def get_products(self, product_ids: list[str]) -> list[Product]:
        client: AsyncMongoClient[dict[str, any]] | None = None
        product_id_list: list[ObjectId] = []
        final_list = []
        result: Any
        for id in product_ids:
            product_id_list.append(ObjectId(id))
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = db["product"].find({"_id": {"$in": product_id_list}})
        except Exception as e:
            raise Exception(f"An error occurred when getting a list of products: {e}")
        finally:
            if client is not None:
                await client.close()
        if(result is None):
            raise NotFoundError("There is no product")
        async for document in result:
            final_list.append(Product(id=str(document["_id"]), name=document["name"], price=document["price"], category=document["category"], description=document["description"]))
        return final_list