import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from db_control import crud, mymodels_MySQL
from dotenv import load_dotenv

# 開発環境の場合のみ.envファイルを読み込む
if os.path.exists(".env"):
    load_dotenv()
else:
    # Azureの環境変数が利用可能であることをログに記録
    print("Running in Azure environment, using system environment variables")

class Customer(BaseModel):
    customer_id: str
    customer_name: str
    age: int
    gender: str

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://tech0-gen-9-step3-1-py-17.azurewebsites.net",  # Azure Web Appのドメイン
        os.getenv("ALLOWED_ORIGINS", "").split(",")  # 環境変数から追加のオリジンを読み込む
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ヘルスチェックエンドポイント
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def index():
    return {"message": "FastAPI top page!"}

@app.post("/customers")
async def create_customer(customer: Customer):
    try:
        values = customer.dict()
        tmp = crud.myinsert(mymodels_MySQL.Customers, values)
        result = crud.myselect(mymodels_MySQL.Customers, values.get("customer_id"))
        
        if result:
            result_obj = json.loads(result)
            return result_obj if result_obj else None
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers")
async def read_one_customer(customer_id: str = Query(...)):
    try:
        result = crud.myselect(mymodels_MySQL.Customers, customer_id)
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        result_obj = json.loads(result)
        return result_obj[0] if result_obj else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/allcustomers")
async def read_all_customer():
    try:
        result = crud.myselectAll(mymodels_MySQL.Customers)
        # 結果がNoneの場合は空配列を返す
        if not result:
            return []
        # JSON文字列をPythonオブジェクトに変換
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/customers")
async def update_customer(customer: Customer):
    try:
        values = customer.dict()
        values_original = values.copy()
        tmp = crud.myupdate(mymodels_MySQL.Customers, values)
        result = crud.myselect(mymodels_MySQL.Customers, values_original.get("customer_id"))
        
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        result_obj = json.loads(result)
        return result_obj[0] if result_obj else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/customers")
async def delete_customer(customer_id: str = Query(...)):
    try:
        result = crud.mydelete(mymodels_MySQL.Customers, customer_id)
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {"customer_id": customer_id, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fetchtest")
async def fetchtest():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users')
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 開発環境での直接実行用
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True  # 開発環境でのみTrue
    )