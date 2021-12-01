from enum import Enum
from typing import Optional

import uvicorn
from fastapi import FastAPI , Request
from pydantic import BaseModel
import threading


app = FastAPI()


class ModelName(str, Enum):

    alexnet = "alexnet"

    resnet = "resnet"

    lenet = "lenet"


    

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    print("helllo")
    return fake_items_db[skip : skip + limit]


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, qu : str, q: str = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id , "quality":qu}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item



@app.get("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item


if __name__ == "__main__":
    uvicorn.run(app ,host="localhost", port=5000,access_log=False)#, reload=True, )

print(input("please enter int"))
