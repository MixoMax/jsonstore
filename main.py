from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import uvicorn
import uuid
import json
import os
import sys

PORT = 1960
HOST = "0.0.0.0"

KB = 1024
MB = 1024 * KB
GB = 1024 * MB

MAX_UPLOAD_SIZE = 100 * MB


app = FastAPI()


@app.get("/get")
async def get(id: str):
    fp = f"./data/{id}.json"
    try:
        with open(fp, "r") as f:
            data = json.load(f)
        
        return JSONResponse(content=data, status_code=200)
    except:
        return JSONResponse(content={"error": "Not found"}, status_code=404)

@app.post("/upload")
async def upload(request: Request):
    data = await request.json()

    is_valid = False
    while not is_valid:
        id = str(uuid.uuid4())
        fp = f"./data/{id}.json"
        if not os.path.exists(fp):
            is_valid = True
    
    size = sys.getsizeof(data)
    if size > MAX_UPLOAD_SIZE:
        return JSONResponse(content={"error": "File too large"}, status_code=400)

    with open(fp, "w") as f:
        json.dump(data, f, indent=4)
    
    return JSONResponse(content={"id": id}, status_code=200)

@app.get("/kv_upload")
async def kv_upload(k: str, v: str):
    with open("./data/_kv.json", "r") as f:
        data = json.load(f)
    
    keys = list(data.keys())
    if k in keys:
        return JSONResponse(content={"error": "Key exists"}, status_code=400)
    
    data[k] = v

    with open("./data/_kv.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return JSONResponse(content={"status": "OK"}, status_code=200)

@app.get("/kv_get")
async def kv_get(k: str):
    with open("./data/_kv.json", "r") as f:
        data = json.load(f)
    
    if k not in data:
        return JSONResponse(content={"error": "Key not found"}, status_code=404)
    
    return JSONResponse(content={"value": data[k]}, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)