from fastapi import FastAPI, Response, status
from starlette.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import uuid

app = FastAPI()

class Item(BaseModel):
    user_id : str = Field(title = '사용자가 사용할 ID')
    password : str = Field(title= '사용자가 사용할 password')

class PatchItem(BaseModel):
    user_id: Optional[str] = Field(None, title='사용자가 사용할 ID')
    password: Optional[str] = Field(None, title='사용자가 사용할 password')

class ResponseItem(Item):
    success: bool = Field(True, title='처리 여부/결과')


@app.get("/health")
async def health_check():
    return {"msg":"Hello World"}

@app.get("/{name}", name="사용자 ID 생성", description="사용자 이름을 받고 ID를 생성하는 API 입니다.")
async def generate_id_for_name(name: str):
    return JSONResponse({
        'id': str(uuid.uuid4()),
        'name': name
    })

@app.post("/register", response_model = ResponseItem)
async def register_item(item: Item):
    dicted_item = dict(item)
    dicted_item['success'] = True
    return JSONResponse(dicted_item)


@app.put("/update")
async def update_item(item: Item):
    dicted_item = {k:v for k, v in dict(item.items())}
    dicted_item['success'] = True
    return JSONResponse(dicted_item)

@app.patch("/update")
async def update_item_sub(item: PatchItem):
    dicted_item = {}
    for k, v in dict(item).items():
        if v:
            dicted_item[k] = v
    dicted_item['success'] = True

    return JSONResponse(dicted_item)

@app.delete("/delete")
async def delete_item():
    dicted_item = None
    return Response(status_code=status.HTTP_204_NO_CONTENT)