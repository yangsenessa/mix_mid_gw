from typing import Union

from fastapi import FastAPI
from .api import usermanner_endpoint

app = FastAPI()

app.include_router(usermanner_endpoint.router)
#app.include_router(items.router)
#app.include_router(
 #   admin.router,
  #  prefix="/admin",
   # tags=["admin"],
   # dependencies=[Depends(get_token_header)],
  #  responses={418: {"description": "I'm a teapot"}},
#)
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]