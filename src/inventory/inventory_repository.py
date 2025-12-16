from .inventory import Inventory
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from pymongo.results import InsertOneResult, UpdateResult
from bson.objectid import ObjectId
from ..customError import NotFoundError
from typing import Any

class InventoryRepository:
    def __init__(self):
        self.url="mongodb+srv://eacmomo0927_db_user:vKaA49hxWXGLdVe8@mycluster.9cvhjpt.mongodb.net/?appName=MyCluster"
    async def add_inventory(self, name: str, location: str) -> str:
        client: AsyncMongoClient[dict[str, any]] | None = None
        result: InsertOneResult | None = None
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = await db["inventory"].insert_one({"name": name, "location": location})
        except Exception as e:
            raise Exception(f"An error occured when creating inventory for {name}: {e}")
        finally:
            if(client is not None):
                await client.close()
        
        return str(result.inserted_id)
    async def get_inventory(self, inventory_id: str) -> Inventory:
        key = ObjectId(inventory_id)
        client: AsyncMongoClient[dict[str, Any]] | None = None
        result: dict | None
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = await db["inventory"].find_one({"_id": key})
        except Exception as e:
            raise Exception(f"error occured when searching {inventory_id}: {e}")
        finally:
            if(client is not None):
                await client.close()
        if(result is None):
            raise NotFoundError(f"Inventory with id {inventory_id} not found")
        return Inventory(id=str(result["_id"]), name=result["name"], location=result["location"], products=result.get("products"))
    
    async def get_inventories(self) -> list[Inventory]:
        client: AsyncMongoClient[dict[str, Any]] | None = None
        result: Any
        final_list = []
        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi('1'))
            db = client["OnlineShop"]
            result = db["inventory"].find({})
        except Exception as e:
            raise Exception(f"An error occurred when getting all inventories: {e}")
        finally:
            if client is not None:
                await client.close()

        if result is None:
            return []
        async for document in result:
            final_list.append(Inventory(id=str(document["_id"]), name=document["name"], location=document["location"], products=document.get("products")))

        return final_list
    
    async def update_product_count(self, inventory_id: str, product_id: str, quantity: int, createDic: bool)->bool:
        client: AsyncMongoClient[dict[str, Any]] | None = None
        result: UpdateResult | None = None

        try:
            client = AsyncMongoClient(self.url, server_api=ServerApi("1"))
            db=client["OnlineShop"]
            query_filter = {"_id": ObjectId(inventory_id)}
            update_operation = {"$set": {"products": {product_id: quantity}}} if createDic else {"$set" : {"products." + product_id: quantity}}
            result = await db["inventory"].update_one(filter=query_filter, update=update_operation)
        except Exception:
            raise Exception(f"An error occurred when updating product count for : {inventory_id} - {product_id}")
        finally:
            if client is not None:
                await client.close()
        if(result is None):
            raise Exception(f"An error occurred when updating product count for : {inventory_id} - {product_id}")
        return result.modified_count == 1
            