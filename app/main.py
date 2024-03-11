from typing import Union

from fastapi import FastAPI
from .api import apiusermanner_endpoint

app = FastAPI()

app.include_router(apiusermanner_endpoint.router)
#app.include_router(items.router)
#app.include_router(
 #   admin.router,
  #  prefix="/admin",
   # tags=["admin"],
   # dependencies=[Depends(get_token_header)],
  #  responses={418: {"description": "I'm a teapot"}},
#)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}